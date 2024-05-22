import asyncio

from fastapi import Depends, FastAPI
import fastapi_users
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from authentication.data_base import User
from authentication.schemas import UserCreate, UserRead
from authentication.user_manager import get_user_manager
from config import setting
from authentication.authentication import auth_backend
from dataBase.operationDataBase import *
from typing import Annotated
from Models.models import Vacancy
engine = create_async_engine(
    url=setting.DATABASE_URL_asyncpg, pool_size=5, max_overflow=10
)

session_factory = async_sessionmaker(engine)
app = FastAPI()


fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, Annotated[UserCreate,Depends()]),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, Annotated[UserCreate,Depends()]),
    prefix="/user",
    tags=["user"],
)

@app.get("/")
async def get_main_page():
    """the first page every visitor sees"""
    return "Welcome to haha.ru! fsddd"

@app.post("/vacancy")
async def create_vacancy(vac: Annotated[Vacancy,Depends()], user: User = Depends(current_active_verified_user)):
    async with session_factory() as session:
        newVac = db.Vacancy(**dict(vac))
        newVac.user_id = user.id
        session.add_all([newVac])
        await session.commit()

    return dict(vac)





@app.get("/profile/me")
async def protected_route(user: User = Depends(current_user)):
    async with session_factory() as session:        
        role_ = await session.get(db.Role, user.role_id)
        return f"Hello, {user.username}, your role is {role_.role_name if role_ else 'slave'}"

@app.get("/profile/{user_login}")
async def get_main_page(user_login: str):
    async with session_factory() as session:
            
        res_ = await session.execute(select(db.User).where(db.User.login == user_login))
        res_ = res_.scalars().all()

        if(len(res_) == 0):
            return None
        return [i.__dict__ for i in res_]





async def main():
    # await erase_data(session_factory, db.User)
    # await insert_data(session_factory)
    # await print_data(session_factory, db.User)
    # await create_role(session_factory)
    pass




if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

