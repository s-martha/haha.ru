import asyncio

from fastapi import Depends, FastAPI, APIRouter
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
from Models.models import *
engine = create_async_engine(
    url=setting.DATABASE_URL_asyncpg, pool_size=5, max_overflow=10
)

session_factory = async_sessionmaker(engine)
app = FastAPI()
router = APIRouter()

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

@router.post("/create", tags=["vacancy"])
async def create_vacancy(vacancy: Annotated[VacancyCreate,Depends()], user: User = Depends(current_active_verified_user)):
    async with session_factory() as session:
        newVac = db.Vacancy(**dict(vacancy))
        newVac.user_id = user.id
        session.add_all([newVac])
        await session.commit()

    return dict(vacancy)

@router.delete("/delete", tags=["vacancy"])
async def delete_vacancy(vacancy: Annotated[VacancyDelete,Depends()]):
    async with session_factory() as session:
        res_ = await session.get(db.Vacancy, vacancy.id)
        if res_ is None:
            return "Vacancy isn't found"
        await session.delete(res_)
        await session.commit()
    return "Vacancy successfully deleted"
@router.get("/filter", tags=["vacancy"])
async def search_vacancy(vacancy: Annotated[VacancySearch,Depends()]):
    async with session_factory() as session:
        query = select(db.Vacancy)
        conditions = []

        if vacancy.id is not None:
            conditions.append(db.Vacancy.id == vacancy.id)
        if vacancy.title is not None:
            conditions.append(db.Vacancy.title == vacancy.title)
        if vacancy.salrayGreaterOrEqual is not None:
            conditions.append(db.Vacancy.salary >= vacancy.salrayGreaterOrEqual)
        if vacancy.user_id is not None:
            conditions.append(db.Vacancy.user_id == vacancy.user_id)
        if vacancy.company_id is not None:
            conditions.append(db.Vacancy.company_id == vacancy.company_id)

        if conditions:
            query = query.where(*conditions)

        result = await session.execute(query)
        vacancies = result.scalars().all()
        return vacancies


@router.post("/addResume", tags=["resume"])
async def create_resume(resume: Annotated[ResumeCreate,Depends()], user: User = Depends(current_active_verified_user)):
    async with session_factory() as session:
        newResume = db.Resume(**dict(resume))
        newResume.user_id = user.id
        session.add(newResume)
        await session.commit()

    return dict(resume)

@router.delete("/delResume", tags=["resume"])
async def delete_resume(resume: Annotated[ResumeDelete,Depends()], user: User = Depends(current_active_verified_user)):
    async with session_factory() as session:

        res_ = await session.get(db.Resume,resume.id)

        if res_ is None:
            return "Resume isn't found"
        await session.delete(res_)
        await session.commit()
    return "Resume successfully deleted"

@router.get("/findResume", tags=["resume"])
async def find_resumes(resume : Annotated[ResumeSearch,Depends()]):
    async with session_factory() as session:
        query = select(db.Resume).where(db.Resume.user_id == resume.user_id)

        result = await session.execute(query)
        resumes = result.scalars().all()

        return resumes


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





app.include_router(router)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

