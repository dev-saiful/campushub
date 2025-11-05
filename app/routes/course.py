from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import engine
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseRead
from app.models.teacher import Teacher
from app.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api/v1/courses", tags=["Courses"])
security = HTTPBearer()

def get_session():
    with Session(engine) as session:
        yield session

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return decode_access_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(data: CourseCreate, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if data.teacher_id:
        teacher = session.get(Teacher, data.teacher_id)
        if not teacher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    course = Course(**data.model_dump())
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

@router.get("/", response_model=list[CourseRead])
def list_courses(session: Session = Depends(get_session), user=Depends(get_current_user)):
    return session.exec(select(Course)).all()
