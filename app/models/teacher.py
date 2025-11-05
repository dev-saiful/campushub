from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

from app.models.course import Course

class Teacher(SQLModel, table=True):
     id: Optional[int] = Field(default=None, primary_key=True)
     name: str
     email: str
     designation: str
     department: str
     joined_at: datetime = Field(default_factory=datetime.now)

     courses: List["Course"] = Relationship(back_populates="teacher")