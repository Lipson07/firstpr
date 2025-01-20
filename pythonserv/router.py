from fastapi import FastAPI,HTTPException,Depends
from typing import Annotated
from pydantic import BaseModel
import uvicorn
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
app = FastAPI()
engine=create_async_engine('sqlite+aiosqlite:///data.db')
new_session=async_sessionmaker(engine,expire_on_commit=False)
async def get_session():
    async with new_session() as session:
        yield session
Session=Annotated[AsyncSession,Depends(get_session)]
class Base(DeclarativeBase):
    pass
class Data(Base):
    __tablename__='data'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]
    password:Mapped[str]
@app.post("/setup_db")
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return{"status":"ok"}
class data_scheme_add(BaseModel):
    name:str
    password:str
class data_scheme(data_scheme_add):
    id:int

@app.post("/data")
async def add_data(a:data_scheme_add,session:Session):
    new_data=Data(
        name=a.name,
        password=a.password
    )
    session.add(new_data)
    await session.commit()
    return{"status":"ok"}
   
@app.get("/data")
async def get_data(session:Session):
  query=select(Data)
  result=await session.execute(query)
  return result.scalars().all()
if __name__== "__main__":
    uvicorn.run(app="main:app",reload=True)