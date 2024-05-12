from typing import Annotated, AsyncGenerator, Optional

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Boolean, select, func

from config import setting
from dataBase.models import Company, Role

DATABASE_URL = setting.DATABASE_URL_asyncpg
base_id = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass

class MySQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    async def get_by_login(self, login: str) -> Optional[int]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.login) == func.lower(login)
        )
        return await self._get_user(statement)

class User(SQLAlchemyBaseUserTable[int], Base):
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    id: Mapped[base_id]
    username: Mapped[str]
    role_id: Mapped[int | None] =  mapped_column(ForeignKey(Role.id))
    hr_company_id: Mapped[int | None] = mapped_column(ForeignKey(Company.id))
    login: Mapped[str]



engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield MySQLAlchemyUserDatabase(session, User)