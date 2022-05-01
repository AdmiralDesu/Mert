from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint, Column, String


class UserBase(SQLModel):
    username: str
    password: str


class User(UserBase, table=True):
    user_id: int = Field(nullable=False, primary_key=True)
    fullname: str = Field(default=None)

    __table_args__ = {'schema': 'users'}


class UserCreate(UserBase):
    pass


class UserCustomize(UserBase):
    fullname: Optional[str] = None


class UserLogin(SQLModel):
    username: str
    password: str

