from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.core.database import engine
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse 
from app.core.security import create_access_token, verify_password, hash_password

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

# Dependecy for getting DB session
def get_session():
    with Session(engine) as session:
        yield session

@router.post("/register", response_model=TokenResponse)
def register_user(data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pass = hash_password(data.password)
    user = User(name=data.name, email=data.email, hashed_password=hashed_pass, role=data.role)
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token({"sub":str(user.id), "role": user.role})
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login_user(data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub":str(user.id), "role": user.role})
    return TokenResponse(access_token=token)