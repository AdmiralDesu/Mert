from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(nullable=False, index=True)
    password: str = Field(nullable=False)


class User(UserBase, table=True):
    user_id: int = Field(nullable=False, primary_key=True)
    fullname: str = Field(default=None)


class UserCreate(UserBase):
    pass


class UserCustomize(UserBase):
    fullname: Optional[str] = Field(default=None)


class UserLogin(SQLModel):
    username: str
    password: str

