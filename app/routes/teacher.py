from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from app.core.database import engine
from app.core.security import decode_access_token
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherRead

router = APIRouter(prefix="/api/v1/teachers", tags=["Teachers"])
security = HTTPBearer()


def get_session():
    with Session(engine) as session:
        yield session


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return decode_access_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.post("/", response_model=TeacherRead, status_code=status.HTTP_201_CREATED)
def create_teacher(
    data: TeacherCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    teacher = Teacher(**data.model_dump())
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return teacher


@router.get("/", response_model=list[TeacherRead])
def list_teachers(
    session: Session = Depends(get_session), user=Depends(get_current_user)
):
    return session.exec(select(Teacher)).all()


@router.get("/{teacher_id}", response_model=TeacherRead)
def get_teacher(
    teacher_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher
