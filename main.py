from fastapi import FastAPI
from db import engine, Base
from routes import auth_routes, protected, student_routes, teacher_routes
from auth import router as auth_router

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db import engine, Base
from routes import auth_routes, protected, student_routes, teacher_routes
from logic import student_logic, teacher_logic
from auth import router as auth_router


app = FastAPI()
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(student_routes.router)
app.include_router(teacher_routes.router)

app.include_router(student_logic.router)
app.include_router(teacher_logic.router)

app.include_router(auth_routes.router)
app.include_router(auth_router)
