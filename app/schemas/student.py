from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    email: EmailStr
    student_id: str
    department: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None

class StudentRead(StudentBase):
    id: int
    joined_at: datetime

    class Config:
        from_attributes = True