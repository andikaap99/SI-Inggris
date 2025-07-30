# auth.py
from fastapi import FastAPI, Request, Form, Depends, Cookie, HTTPException, status
from fastapi import APIRouter
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from db import SessionLocal, get_db
from models import User, Student, Teacher
from sqlalchemy.orm import Session

SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    scheme, _, param = token.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token scheme")

    try:
        payload = jwt.decode(param, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def role_required(required_role: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this resource"
            )
        return current_user
    return role_checker

@router.get("/check-session")
def check_session(current_user: dict = Depends(get_current_user)):
    return {"status": "ok"}

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    return current_user

@router.get("/api/me")
def get_user_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user["username"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    role = user.role
    profile_data = {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }

    if role == "student":
        student = db.query(Student).filter(Student.user_id == user.id).first()
        if student:
            profile_data.update({
                "name": student.name,
                "class_name": student.class_name,
                "total_score": student.total_score or 0
            })
    elif role == "teacher":
        teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
        if teacher:
            profile_data.update({
                "name": teacher.name
            })

    return profile_data
