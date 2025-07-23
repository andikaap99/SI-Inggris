# routes/auth_routes.py
from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import get_db
from models import User
from auth import hash_password, verify_password, create_access_token

from fastapi import APIRouter

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "result": None})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "result": None})

@router.post("/try-login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    print("Input Username:", username)
    print("User Found:", user is not None)
    if user:
        print("Stored Hash:", user.hashed_password)
        print("Password Match:", verify_password(password, user.hashed_password))

    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Username atau password salah"
        }, status_code=401)

    # Buat JWT token
    token = create_access_token(data={
        "sub": user.username,
        "role": user.role
    })

    # Set token ke cookie
    response = RedirectResponse(url="/home", status_code=302)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=7200  # 2 jam
    )
    return response

@router.post("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response
