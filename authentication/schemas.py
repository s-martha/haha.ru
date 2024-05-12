
from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    role_id: int | None
    hr_company_id: int | None
    login: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    login: str
    password: str
    username: str
    role_id: Optional[int] = 1
    hr_company_id: Optional[int] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    password: str| None = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
    role_id: Optional[int] = 1
    hr_company_id: Optional[int] = None