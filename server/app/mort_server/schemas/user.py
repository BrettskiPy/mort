from typing import Optional

from pydantic import BaseModel, EmailStr


# Attributes Shared by all User schemas
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


# Attributes to receive on User creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Attributes to receive on User update
class UserUpdate(UserBase):
    password: Optional[str] = None


# A full user representation, can include DB fields
class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties that are stored in the DB, but that won't be returned via API
class UserInDB(User):
    hashed_password: str
