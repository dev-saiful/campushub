from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    code: str
    title: str
    credit: float

class CourseCreate(CourseBase):
    teacher_id: Optional[int] = None

class CourseRead(CourseBase):
    id: int
    teacher_id: Optional[int] = None

    class Config:
        from_attributes = True
