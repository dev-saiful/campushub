from fastapi import FastAPI
from app.core.database import init_db
from contextlib import asynccontextmanager
from app.routes import auth, course, student, teacher

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# reassign app to use the new lifespan manager
app = FastAPI(title="CampusHub API", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(course.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the CampusHub API!🚀"}
