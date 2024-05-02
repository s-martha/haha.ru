from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import setting

engine = create_engine(
    url=setting.DATABASE_URL_psycopg, pool_size=5, max_overflow=10
)

session_factory = sessionmaker(engine)

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'autoload_with':engine}

class Companies(Base):
    __tablename__ = 'companies'
    __table_args__ = {'autoload_with':engine}


class Communication(Base):
    __tablename__ = 'communication'
    __table_args__ = {'autoload_with':engine}


class Vacancies(Base):
    __tablename__ = 'vacancies'
    __table_args__ = {'autoload_with':engine}


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'autoload_with':engine}


class Resumes(Base):
    __tablename__ = 'resumes'
    __table_args__ = {'autoload_with':engine}


