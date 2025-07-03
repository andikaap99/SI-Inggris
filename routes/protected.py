# routes/protected.py
from fastapi import FastAPI, Request, Form, Depends, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth import decode_access_token
from db import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from db import get_db
from models import User
from auth import get_current_user, admin_required

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/home", response_class=HTMLResponse)
async def read_root(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("home.html", {"request": request, "result": None})


# @router.get("/listening-word", response_class=None)
# def listening_app(request: Request, current_user: dict = Depends(admin_required)):
 
#     return templates.TemplateResponse("listening-word/Menu.html", {"request": request})
