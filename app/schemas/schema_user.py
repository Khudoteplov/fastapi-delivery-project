from pydantic import (BaseModel, Field, BeforeValidator, EmailStr)
from pydantic_settings import SettingsConfigDict
from typing import Optional, Annotated, TypeAlias
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field as SQLField


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    user_id: int = SQLField(default=None, nullable=False, primary_key=True)
    email: str = SQLField(nullable=True, unique_items=True)
    password: str | None
    name: str
    x: float
    y: float

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Иван Иванов",
                "email": "user@example.com",
                "password": "qwerty",
                "x": 0.0 ,
                "y": 0.0
            }
        }


class Courier(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    courier_id: int = SQLField(default=None, nullable=False, primary_key=True)
    email: str = SQLField(nullable=True, unique_items=True)
    password: str | None
    name: str
    x: float | None
    y: float | None
    max_number: int
    current_number: int | None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Иван Иванов",
                "email": "user@example.com",
                "password": "qwerty",
                "max_number": 10
            }
        }



