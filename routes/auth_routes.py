# routes/auth_routes.py
from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db import SessionLocal, get_db
from models import User
from auth import hash_password, verify_password, create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")



@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse("login.html", {"request": request, "result": None})


from fastapi.responses import RedirectResponse

@router.post("/login")
async def login(request: Request, nis: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nis == nis).first()

    print("Input NIS:", nis)
    print("User Found:", user is not None)
    if user:
        print("Stored Hash:", user.hashed_password)
        print("Password Match:", verify_password(password, user.hashed_password))


    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "NIS atau password salah"}, status_code=401)

    token = create_access_token(data={
    "sub": user.nis,
    "role": user.role
    })

    response = RedirectResponse(url="/home", status_code=302)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800  
    )
    return response

@router.post("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response


