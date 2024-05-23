from pydantic import BaseModel

class Base(BaseModel):
    pass



class VacancyCreate(Base):
    title: str
    salary: int
    descriprion: str | None
    contacts: str | None

class VacancyUpdate(Base):
    id: int

class VacancySearch(Base):
    id: int | None = None
    user_id: int | None = None
    company_id: int | None = None
    title: str | None = None
    salrayGreaterOrEqual: int | None = None

