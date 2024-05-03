from typing import Annotated
from sqlalchemy import create_engine, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from config import setting

engine = create_engine(
    url=setting.DATABASE_URL_psycopg, pool_size=5, max_overflow=10
)

session_factory = sessionmaker(engine)

Base = declarative_base()

base_id = Annotated[int, mapped_column(primary_key=True)]

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[base_id]
    username: Mapped[str]
    role_id: Mapped[int] =  mapped_column(ForeignKey("roles.id"))
    hr_company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    verified: Mapped[bool]
    login: Mapped[str]
    password_hash: Mapped[int]

class Companies(Base):
    __tablename__ = 'companies'
    id: Mapped[base_id]
    name: Mapped[str]
    inn: Mapped[str]
    description: Mapped[str] = mapped_column(Text())
    verified: Mapped[bool]   


class Communication(Base):
    __tablename__ = 'communication'
    id: Mapped[base_id]
    vacancy_id: Mapped[int]
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id")) 


class Vacancies(Base):
    __tablename__ = 'vacancies'
    id: Mapped[base_id]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("compamies.id")) 
    title: Mapped[str]
    salary: Mapped[int]
    descriprion: Mapped[str] = mapped_column(Text())
    contacts: Mapped[str]


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[base_id]
    role_name: Mapped[str]


class Resumes(Base):
    __tablename__ = 'resumes'
    id: Mapped[base_id]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str]
    descriprion: Mapped[str] = mapped_column(Text())
    contacts: Mapped[str]


