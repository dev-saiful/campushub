from datetime import datetime
from pydantic import BaseModel, EmailStr


class TeacherBase(BaseModel):
    name: str
    email: EmailStr
    designation: str
    department: str


class TeacherCreate(TeacherBase):
    pass


class TeacherRead(TeacherBase):
    id: int
    joined_at: datetime

    class Config:
        from_attributes = True
