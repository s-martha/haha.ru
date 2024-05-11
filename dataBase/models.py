from typing import Annotated
from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

base_id = Annotated[int, mapped_column(primary_key=True)]

class Company(Base):
    __tablename__ = 'company'
    id: Mapped[base_id]
    name: Mapped[str]
    inn: Mapped[str | None]
    description: Mapped[str] = mapped_column(Text())
    verified: Mapped[bool] = mapped_column(default= False)

class Role(Base):
    __tablename__ = 'role'
    id: Mapped[base_id]
    role_name: Mapped[str]

class User(Base):
    __tablename__ = 'user'
    id: Mapped[base_id]
    username: Mapped[str]
    role_id: Mapped[int | None] =  mapped_column(ForeignKey(Role.id))
    hr_company_id: Mapped[int | None] = mapped_column(ForeignKey(Company.id))
    login: Mapped[str]
    hashed_password: Mapped[int]
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


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id: Mapped[base_id]
    user_id: Mapped[int | None] = mapped_column(ForeignKey(User.id))
    company_id: Mapped[int | None] = mapped_column(ForeignKey(Company.id)) 
    title: Mapped[str]
    salary: Mapped[int | None]
    descriprion: Mapped[str | None] = mapped_column(Text())
    contacts: Mapped[str]

class Resume(Base):
    __tablename__ = 'resume'
    id: Mapped[base_id]
    user_id: Mapped[int | None] = mapped_column(ForeignKey(User.id))
    title: Mapped[str]
    descriprion: Mapped[str] = mapped_column(Text())
    contacts: Mapped[str]


class Communication(Base):
    __tablename__ = 'communication'
    id: Mapped[base_id]
    vacancy_id: Mapped[int | None] = mapped_column(ForeignKey(Vacancy.id)) 
    resume_id: Mapped[int | None] = mapped_column(ForeignKey(Resume.id)) 
