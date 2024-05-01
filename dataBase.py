from sqlalchemy import create_engine, text, MetaData, Text,  Table, Integer, String, Boolean,BigInteger,\
    Column, DateTime, ForeignKey, Numeric, CheckConstraint, insert
from config import setting

engine = create_engine(
    url=setting.DATABASE_URL_psycopg, echo=True, pool_size=5, max_overflow=10
)



metadata = MetaData()

# CREATE TABLE "users" (
#   "id" integer PRIMARY KEY,
#   "username" varchar,
#   "role_id" integer,
#   "hr_company_id" integer,
#   "verified" bool,
#   "login" varchar,
#   "password_hash" bigint
# );
users = Table('users', metadata,
    Column('id', Integer(), primary_key=True),
    Column('username', String(200), nullable=False),
    Column('role_id', Integer(), ForeignKey("roles.id")),
    Column('hr_company_id', Integer(), ForeignKey("companies.id")),
    Column('verified', Boolean()),
    Column('login', String(200), nullable=False),
    Column('password_hash', BigInteger(), nullable=False),
)

# CREATE TABLE "resumes" (
#   "id" integer PRIMARY KEY,
#   "user_id" integer,
#   "title" varchar,
#   "descriprion" text,
#   "contacts" varchar
# );
resumes = Table('resumes', metadata,
    Column('id', Integer(), primary_key=True),
    Column('user_id', Integer(), ForeignKey("users.id")),
    Column('title', String(200),  nullable=False),
    Column('descriprion', Text(),  nullable=False),
    Column('contacts', String(200),  nullable=False),
)
# CREATE TABLE "role" (
#   "id" integer PRIMARY KEY,
#   "role_name" varchar
# );
roles = Table('roles', metadata,
    Column('id', Integer(), primary_key=True),
    Column('role_name', String(200),  nullable=False),
)

# CREATE TABLE "vacancies" (
#   "id" integer PRIMARY KEY,
#   "user_id" integer,
#   "company_id" integer,
#   "title" varchar,
#   "salary" integer,
#   "descriprion" text,
#   "contacts" varchar
# );
vacancies = Table('vacancies', metadata,
    Column('id', Integer(), primary_key=True),
    Column('user_id', Integer(), ForeignKey("users.id")),
    Column('company_id', Integer(), ForeignKey("companies.id")),
    Column('title', String(200),  nullable=False),
    Column('descriprion', Text(), nullable=False),
    Column('salary', Integer()),
    Column('contacts', String(200), nullable=False),
)

# CREATE TABLE "communication" (
#   "id" integer PRIMARY KEY,
#   "vacancy_id" integey
#   "resume_id" integer
# );
communication = Table('communication', metadata,
    Column('id', Integer(), primary_key=True),
    Column('vacancy_id', Integer(), ForeignKey("vacancies.id")),
    Column('resume_id', Integer(), ForeignKey("resumes.id")),
)

# CREATE TABLE "companies" (
#   "id" integer PRIMARY KEY,
#   "name" varchar,
#   "inn" varchar,
#   "description" varchar,
#   "verified" bool
# );
companies = Table('companies', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(200),  nullable=False),
    Column('inn', String(200),  nullable=False),
    Column('descriprion', Text(), nullable=False),
    Column('verified', Boolean()),
)


metadata.drop_all(engine)
metadata.create_all(engine)


with engine.connect() as conn:
    res = conn.execute(text("Select 1, 2, 3"))
    print(f"{res.all()=}")

    stmt = insert(users).values(
        [
            {"username": "IIeJIbMeHb", "login": "IIeJIbMeHb2005", "password_hash" : 14522},
            {"username": "Nagibator3000", "login": "NagibatorDA", "password_hash" : 2005},

        ]
    )

    conn.execute(stmt)
    conn.commit()