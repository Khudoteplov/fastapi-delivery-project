from pydantic import (BaseModel, Field)
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field as SQLField


class Order(SQLModel, BaseModel, table=True):
    order_id: int = SQLField(default=None, nullable=False, primary_key=True)
    x: float
    y: float
    amount: int

