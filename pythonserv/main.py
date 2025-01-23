from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError
import uvicorn
from typing import Annotated, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
engine = create_async_engine('sqlite+aiosqlite:///data.db')
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class Data(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]


async def create_db_if_not_exists():
    async with engine.begin() as conn:
          await conn.run_sync(Base.metadata.create_all)


class data_scheme_add(BaseModel):
    name: str
    password: str


class data_scheme(data_scheme_add):
    id: int


app.mount("/static", StaticFiles(directory="frontend"), name="static")

templates = Jinja2Templates(directory="frontend")


@app.on_event("startup")
async def startup_event():
     await create_db_if_not_exists()
admin=data_scheme_add(name="admin",password="admin")
@app.post("/registr")
async def add_data(a: data_scheme_add, session: Session):
    try:
        print("Received Data:", a.model_dump())
        
        query = select(Data).where(Data.name == a.name)
     
     
        result_name = await session.execute(query)

        existing_user = result_name.scalar_one_or_none()

  
        
       

        if existing_user and existing_user.password == a.password:
           if existing_user.name==admin.name:
               return  {"status": "ok", "name": existing_user.name, "password": existing_user.password,"user":admin}
           print("User already exists:", existing_user.name)
       
           return {"status": "ok", "name": existing_user.name, "password": existing_user.password}
        elif existing_user and existing_user.password != a.password:
            return {"status": "error", "message": "Invalid password"}
        else:
          
            new_data = Data(
              name=a.name,
              password=a.password
              )
            session.add(new_data)
            await session.commit()
            print("User created", a.name)
            return {"status": "ok", "name": a.name, "password": a.password}

    except ValidationError as e:
        print(f"Validation Error: {e}")
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        print(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("regestr.html", {"request": request})


@app.get("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get("/bd", response_model=List[str])  
async def bd(session: AsyncSession = Depends(get_session)):
    query = select(Data)
    result = await session.execute(query)
    data_objects = result.scalars().all()

    names = [item.name for item in data_objects]  

    return names
if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
