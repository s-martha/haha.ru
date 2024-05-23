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

