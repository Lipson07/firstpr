   #database_chat.py
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
DATABASE_URL_CHAT = "sqlite+aiosqlite:///chat.db"  # Используйте aiosqlite для асинхронности
engine_chat = create_async_engine(DATABASE_URL_CHAT, connect_args={"check_same_thread": False})
SessionLocalChat = sessionmaker(autocommit=False, autoflush=False, bind=engine_chat,class_=AsyncSession)
print("SessionLocalChat",SessionLocalChat)
BaseChat = declarative_base()
    # Ассоциативная таблица для связи "многие ко многим" между User и Chat
user_chat = Table(
        "user_chat",
        BaseChat.metadata,
        Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
        Column("chat_id", Integer, ForeignKey("chats.id"), primary_key=True),
    )

    # Теперь создаем классы для userchat user chat message
class UserChat(BaseChat):  # Создаем класс UserChat для связи между таблицами
        __tablename__ = "user_chat"
        user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
        chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)
        user = relationship("User", back_populates="chats") # Связь с таблицей User
        chat = relationship("Chat", back_populates="users")   # Связь с таблицей Chat
class User(BaseChat):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True, index=True)
        auth_user_id = Column(String, unique=True, index=True)  #  String, чтобы соответствовать Data.name
        username = Column(String, index=True)
        chats = relationship("Chat", secondary=user_chat, back_populates="users")  # Связь "многие ко многим"
        messages = relationship("Message", back_populates="author")  # Связь с сообщениями
class Chat(BaseChat):
        __tablename__ = "chats"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
        users = relationship("User", secondary=user_chat, back_populates="chats")
        messages = relationship("Message", back_populates="chat")

class Message(BaseChat):
        __tablename__ = "messages"
        id = Column(Integer, primary_key=True, index=True)
        text = Column(String)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
        author_id = Column(Integer, ForeignKey("users.id"))  # ForeignKey на таблицу users
        author = relationship("User", back_populates="messages")
        chat_id = Column(Integer, ForeignKey("chats.id"))  # ForeignKey на таблицу chats
        chat = relationship("Chat", back_populates="messages")

    # async def create_db_if_not_exists_chat():
    #     async with engine_chat.begin() as conn:
    #         await conn.run_sync(BaseChat.metadata.create_all)

async def create_db_if_not_exists_chat():
        async with engine_chat.begin() as conn:
            await conn.run_sync(BaseChat.metadata.create_all)

async def main():
        await create_db_if_not_exists_chat()

if __name__ == "__main__":
        asyncio.run(main())
