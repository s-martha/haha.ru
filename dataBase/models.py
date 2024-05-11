from typing import Annotated
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase



class Base(DeclarativeBase):
    pass

base_id = Annotated[int, mapped_column(primary_key=True)]

class User(Base):
    __tablename__ = 'user'
    id: Mapped[base_id]
    username: Mapped[str]
    role_id: Mapped[int | None] =  mapped_column(ForeignKey("role.id"))
    hr_company_id: Mapped[int | None] = mapped_column(ForeignKey("company.id"))
    verified: Mapped[bool] = mapped_column(default= False)
    login: Mapped[str]
    password_hash: Mapped[int]

class Company(Base):
    __tablename__ = 'company'
    id: Mapped[base_id]
    name: Mapped[str]
    inn: Mapped[str | None]
    description: Mapped[str] = mapped_column(Text())
    verified: Mapped[bool] = mapped_column(default= False)


class Communication(Base):
    __tablename__ = 'communication'
    id: Mapped[base_id]
    vacancy_id: Mapped[int | None] = mapped_column(ForeignKey("vacancy.id")) 
    resume_id: Mapped[int | None] = mapped_column(ForeignKey("resume.id")) 


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id: Mapped[base_id]
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    company_id: Mapped[int | None] = mapped_column(ForeignKey("company.id")) 
    title: Mapped[str]
    salary: Mapped[int | None]
    descriprion: Mapped[str | None] = mapped_column(Text())
    contacts: Mapped[str]


class Role(Base):
    __tablename__ = 'role'
    id: Mapped[base_id]
    role_name: Mapped[str]


class Resume(Base):
    __tablename__ = 'resume'
    id: Mapped[base_id]
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str]
    descriprion: Mapped[str] = mapped_column(Text())
    contacts: Mapped[str]


