from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import engine
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate
from app.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api/v1/students", tags=["Students"])
security = HTTPBearer()

def get_session():
    with Session(engine) as session:
        yield session

def get_current_user(token:HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_access_token(token.credentials)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, session: Session = Depends(get_session), user=Depends(get_current_user)):
    student = Student(**data.model_dump())
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@router.get("/", response_model=list[StudentRead])
def list_students(session: Session = Depends(get_session), user=Depends(get_current_user)):
    students = session.exec(select(Student)).all()
    return students

@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@router.patch("/{student_id}", response_model=StudentRead)
def update_student(student_id:int, data: StudentUpdate, session: Session = Depends(get_session), user = Depends(get_current_user)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"detail": "Student deleted successfully"}