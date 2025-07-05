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
from models import User, Image_Word, Listening_Word, Complete_Sentence, Listening_Sentence, Category_Listening_Word, Category_Listening_Sentence, Category_Image_Word, Category_Complete_Sentence, Attempt_Complete_Sentences, Attempt_Listening_Word, Attempt_Listening_Sentence, Attempt_Image_Word, Global_Attempt
from auth import get_current_user, admin_required

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/home", response_class=HTMLResponse)
async def read_root(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("home2.html", {"request": request, "result": None})

@router.get("/home-leaderboard", response_class=JSONResponse)
def leaderboard_home(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).filter(User.role == "admin")\
                .order_by(User.total_score.desc())\
                .limit(3).all()

    result = []
    for user in users:
        result.append({
            "name": user.name,  
            "score": user.total_score or 0
        })
    return result

@router.get("/profile", response_class=HTMLResponse)
async def read_root(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("profile.html", {"request": request, "result": None})

@router.get("/profile-global-attempts")
def get_user_global_attempts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # pakai dict, bukan User
):
    # Ambil user berdasarkan nis dari token
    user = db.query(User).filter(User.nis == current_user["nis"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Ambil semua global attempt milik user ini
    attempts = db.query(Global_Attempt).filter(Global_Attempt.user_id == user.id).all()

    results = []
    for a in attempts:
        # Cari nama kategori sesuai tipe fitur
        category_name = "-"
        if a.feature_type == "Image_Word":
            category = db.query(Category_Image_Word).filter(Category_Image_Word.Id_ciw == a.category_id).first()
        elif a.feature_type == "Complete_Sentences":
            category = db.query(Category_Complete_Sentence).filter(Category_Complete_Sentence.Id_ccs == a.category_id).first()
        elif a.feature_type == "Listening_Sentence":
            category = db.query(Category_Listening_Sentence).filter(Category_Listening_Sentence.Id_cls == a.category_id).first()
        elif a.feature_type == "Listening_Word":
            category = db.query(Category_Listening_Word).filter(Category_Listening_Word.Id_clw == a.category_id).first()
        else:
            category = None

        if category:
            category_name = category.name

        results.append({
            "feature": a.feature_type.replace("_", " "),
            "category": category_name,
            "score": a.score
        })

    return results

@router.get("/listening-word", response_class=None)
def listening_word(request: Request, current_user: dict = Depends(admin_required)):
 
    return templates.TemplateResponse("listening-word/Menu.html", {"request": request})

@router.get("/listening-word-word", response_class=None)
def listening_word(request: Request, current_user: dict = Depends(admin_required)):

    return templates.TemplateResponse("listening-word/listening-word.html", {"request": request})

@router.get("/listening-sentence",response_class=None)
def listening_sentence(request: Request, current_user: dict = Depends(admin_required)):

    return templates.TemplateResponse("listening-sentence/Menu.html", {"request": request})


@router.get("/listening-sentence-sentence",response_class=None)
def listening_sentence(request: Request, current_user: dict = Depends(admin_required)):

    return templates.TemplateResponse("listening-sentence/listening-sentence.html", {"request": request})


@router.get("/complete-sentence",response_class=None)
def complete_sentence(request: Request, current_user: dict = Depends(admin_required)):

    return templates.TemplateResponse("complete-sentence/Menu.html", {"request": request})


@router.get("/complete-sentence-sentence",response_class=None)
def complete_sentence_sentence(request: Request, current_user: dict = Depends(admin_required)):

    return templates.TemplateResponse("complete-sentence/complete-sentence.html", {"request": request})

@router.get("/image-word",response_class=None)
def image_word(request: Request, current_user: dict = Depends(admin_required)):

    return templates.TemplateResponse("image-word/Menu.html", {"request": request})

@router.get("/image-word-word",response_class=None)
def image_word(request: Request, current_user: dict = Depends(admin_required)):

    return templates.TemplateResponse("image-word/image-word.html", {"request": request})

@router.get("/result",response_class=None)
def request(request: Request, current_user: dict = Depends(admin_required)):

    return templates.TemplateResponse("score/score.html", {"request": request})