from sqlmodel import SQLModel
from typing import TypeVar

TypeSQL = TypeVar("SQLType", bound=SQLModel)