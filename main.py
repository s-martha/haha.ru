import asyncio

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import setting

from dataBase.operationDataBase import *





engine = create_async_engine(
    url=setting.DATABASE_URL_asyncpg, pool_size=5, max_overflow=10
)

session_factory = async_sessionmaker(engine)
app = FastAPI()


@app.get("/")
def get_main_page():
    """the first page every visitor sees"""
    return "Welcome to haha.ru! fsddd"


@app.get("/login")
def get_login_page():
    """page where user enters login and password"""
    return "Login page"


@app.get("/profile/{user_login}")
async def get_main_page(user_login: str):
    # result = {}
    # insert_data()
    async with session_factory() as session:
            
        res_ = await session.execute(select(db.User).where(db.User.login == user_login))
        res = res_.scalars().all()

        if(len(res) == 0):
            return None
        return [{"id": i.id, "username": i.username, "login": i.login} for i in res]

# print_data(session_factory, db.User)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(print_data(session_factory, db.User))