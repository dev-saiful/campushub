
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .teacher import Teacher


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    title: str
    credit: float

    teacher_id: int | None = Field(default=None, foreign_key="teacher.id")
    teacher: Optional["Teacher"] = Relationship(back_populates="courses")
