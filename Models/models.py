from pydantic import BaseModel

class Base(BaseModel):
    pass



class VacancyCreate(Base):
    title: str
    salary: int
    descriprion: str | None
    contacts: str | None

class VacancyDelete(Base):
    id: int

class VacancySearch(Base):
    id: int | None = None
    user_id: int | None = None
    company_id: int | None = None
    title: str | None = None
    salrayGreaterOrEqual: int | None = None



class ResumeCreate(Base):
    title: str
    descriprion: str
    contacts: str
class ResumeDelete(Base):
    id : int
class ResumeSearch(Base):
    user_id : int

