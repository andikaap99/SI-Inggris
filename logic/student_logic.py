from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sentence_transformers import SentenceTransformer, util
from sqlalchemy import func
from sqlalchemy.orm import Session
from db import engine, Base, get_db
from models import User, Student, Image_Word, Listening_Word, Complete_Sentence, Listening_Sentence, Category, Category, Category, Category, Attempt_Complete_Sentence, Attempt_Listening_Word, Attempt_Listening_Sentence, Attempt_Image_Word, Global_Attempt
from datetime import datetime
from auth import get_current_user, role_required


router = APIRouter()
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

similarity_model = SentenceTransformer('./models/model')


## method untuk load leaderboard home
@router.get("/home-leaderboard", response_class=JSONResponse)
def leaderboard_home(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    students = (
        db.query(Student)
        .join(User)
        .filter(User.role == "student")
        .order_by(Student.total_score.desc())
        .limit(3)
        .all()
    )

    result = []
    for student in students:
        result.append({
            "name": student.name,
            "class_name": student.class_name,
            "score": student.total_score or 0
        })

    return result

## method untuk load user attempts
@router.get("/profile-global-attempts")
def get_user_global_attempts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user["username"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    attempts = db.query(Global_Attempt).filter(Global_Attempt.user_id == user.id).all()

    results = []
    for a in attempts:
        category_name = "-"
        if a.feature_type == "Image_Word":
            category = db.query(Category).filter(Category.Id_cat == a.Id_cat).first()
        elif a.feature_type == "Complete_Sentence":
            category = db.query(Category).filter(Category.Id_cat == a.Id_cat).first()
        elif a.feature_type == "Listening_Sentence":
            category = db.query(Category).filter(Category.Id_cat == a.Id_cat).first()
        elif a.feature_type == "Listening_Word":
            category = db.query(Category).filter(Category.Id_cat == a.Id_cat).first()
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


## method untuk save attempt
@router.post("/save-attempt")
async def save_attempt(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    features = data.get("feature")
    student_id = data.get("student_id")
    category_name = data.get("category_id")
    score = data.get("score")

    ## cek apakah data lengkap
    if not student_id or not category_name or score is None:
        return JSONResponse({"error": "Data tidak lengkap"}, status_code=400)

    ## cek kategori
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return JSONResponse({"error": "Kategori tidak ditemukan"}, status_code=404)
    category_id = category.Id_cat

    ## cek user
    user = db.query(User).filter(User.username == student_id).first()
    if not user:
        return JSONResponse({"error": "User tidak ditemukan"}, status_code=404)
    
    tabel = Attempt_Listening_Word
    if features == "Complete_Sentence":
        tabel = Attempt_Complete_Sentence
    elif features == "Image_Word":
        tabel = Attempt_Image_Word
    elif features == "Listening_Sentence":
        tabel = Attempt_Listening_Sentence
    elif features == "Listening_Word":
        tabel = Attempt_Listening_Word

    ## cek apakah udah ada data di db (feature attempt)
    existing_attempt = db.query(tabel).filter(
        tabel.user_id == user.id,
        tabel.Id_cat == category_id
    ).first()

    ## insert atau update data
    if existing_attempt:
        existing_attempt.score = score
        existing_attempt.attempted_at = datetime.utcnow()
    else:
        new_attempt = tabel(
            score=score,
            user_id=user.id,
            Id_cat=category_id
        )
        db.add(new_attempt)

    ## cek apakah udah ada data di db (global attempt)
    existing_global = db.query(Global_Attempt).filter(
        Global_Attempt.user_id == user.id,
        Global_Attempt.Id_cat == category_id,
        Global_Attempt.feature_type == features
    ).first()

    ## insert atau update data
    if existing_global:
        existing_global.score = score
        existing_global.attempted_at = datetime.utcnow()
    else:
        new_global = Global_Attempt(
            score=score,
            user_id=user.id,
            Id_cat=category_id,
            feature_type=features
        )
        db.add(new_global)

    db.flush()

    ## hitung total skor
    total_score = db.query(func.sum(Global_Attempt.score)).filter(
        Global_Attempt.user_id == user.id
    ).scalar() or 0

    if user.role == "student" and user.student:
        user.student.total_score = total_score

    db.commit()

    return {"message": "Attempt berhasil disimpan", "score": score}


# |----- Image Word Section -----|
## method untuk ambil soal pertama
@router.get("/image-word/start/{category_name}")
def start_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return {"error": "Kategori tidak ditemukan"}

    ## ambil soal pertama
    first_question = db.query(Image_Word)\
                       .filter(Image_Word.Id_cat == category.Id_cat)\
                       .order_by(Image_Word.Id_iw).first()

    if first_question:
        return {
            "id_iw": first_question.Id_iw,
            "image_url": first_question.image_iw
        }

    return {"error": "Tidak ada soal untuk kategori ini"}

## method untuk ambil soal berikutnya
@router.get("/image-word/{id_iw}/")
def get_question(id_iw: int, db: Session = Depends(get_db)):
    item = db.query(Image_Word).filter(Image_Word.Id_iw == id_iw).first()
    if item:
        return {
            "id_iw": item.Id_iw,
            "image_url": item.image_iw
        }
    return {"error": "Soal tidak ditemukan"}

## method untuk pengecekan jawaban
@router.post("/image-word/answer/")
async def answer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_iw = data.get("id_iw")
    student_answer = data.get("student_answer", "").strip().lower()

    ## cek soal
    item = db.query(Image_Word).filter(Image_Word.Id_iw == id_iw).first()
    if not item:
        return JSONResponse({"correct": False, "error": "Soal tidak ditemukan"})

    ## cek jawaban
    is_correct = item.iw_answer.strip().lower() == student_answer

    current_category_id = item.Id_cat
    next_item = db.query(Image_Word)\
                  .filter(Image_Word.Id_cat == current_category_id, Image_Word.Id_iw > id_iw)\
                  .order_by(Image_Word.Id_iw).first()

    return {
        "correct": is_correct,
        "next_id": next_item.Id_iw if next_item else None,
        "next_image": next_item.image_iw if next_item else None
    }


# |----- Listening Word Section -----|
# method untuk ambil soal pertama
@router.get("/listening-word/start/{category_name}")
def start_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return {"error": "Kategori tidak ditemukan"}

    ## ambil soal pertama
    first_question = db.query(Listening_Word)\
                       .filter(Listening_Word.Id_cat == category.Id_cat)\
                       .order_by(Listening_Word.Id_lw).first()

    if first_question:
        return {
            "id_lw": first_question.Id_lw,
            "audio_url": first_question.audio_lw
        }

    return {"error": "Tidak ada soal untuk kategori ini"}

## method untuk mengambil soal berikutnya
@router.get("/listening-word/{id_lw}/")
def get_question(id_lw: int, db: Session = Depends(get_db)):
    item = db.query(Listening_Word).filter(Listening_Word.Id_lw == id_lw).first()
    if item:
        return {
            "id_lw": item.Id_lw,
            "audio_url": item.audio_lw,
        }
    
    return {"error": "Soal tidak ditemukan"}

## method untuk pengecekan jawab
@router.post("/listening-word/answer/")
async def answer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_lw = data.get("id_lw")
    student_answer = data.get("student_answer", "").strip().lower()

    ## cek soal
    item = db.query(Listening_Word).filter(Listening_Word.Id_lw == id_lw).first()
    if not item:
        return JSONResponse({"correct": False, "error": "Soal tidak ditemukan"})

    ## cek jawaban
    is_correct = item.lw_answer.strip().lower() == student_answer

    current_category_id = item.Id_cat
    next_item = db.query(Listening_Word)\
                  .filter(Listening_Word.Id_cat == current_category_id, Listening_Word.Id_lw > id_lw)\
                  .order_by(Listening_Word.Id_lw).first()

    return {
        "correct": is_correct,
        "next_id": next_item.Id_lw if next_item else None,
        "next_audio": next_item.audio_lw if next_item else None
    }


# |----- Complete Sentence Section -----|
# method untuk ambil soal pertama
@router.get("/complete-sentence/start/{category_name}")
def start_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return {"error": "Kategori tidak ditemukan"}

    ## ambil soal pertama
    first_question = db.query(Complete_Sentence)\
                       .filter(Complete_Sentence.Id_cat == category.Id_cat)\
                       .order_by(Complete_Sentence.Id_cs).first()

    if first_question:
        return {
            "id_cs": first_question.Id_cs,
            "question": first_question.question_cs
        }

    return {"error": "Tidak ada soal untuk kategori ini"}


## method untuk ambil soal berikutnya
@router.get("/complete-sentence/{id_cs}/")
def get_question(id_cs: int, db: Session = Depends(get_db)):
    item = db.query(Complete_Sentence).filter(Complete_Sentence.Id_cs == id_cs).first()
    if item:
        return {
            "id_cs": item.Id_cs,
            "question": item.question_cs
        }
    return {"error": "Soal tidak ditemukan"}

## method untuk pengecekan jawab
@router.post("/complete-sentence/answer/")
async def answer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_cs = data.get("id_cs")
    student_answer = data.get("student_answer", "").strip().lower()

    ## cek soal
    item = db.query(Complete_Sentence).filter(Complete_Sentence.Id_cs == id_cs).first()
    if not item:
        return JSONResponse({"correct": False, "error": "Soal tidak ditemukan"})

    ## cek jawaban
    is_correct = item.cs_answer.strip().lower() == student_answer

    current_category_id = item.Id_cat
    next_item = db.query(Complete_Sentence)\
                  .filter(Complete_Sentence.Id_cat == current_category_id, Complete_Sentence.Id_cs > id_cs)\
                  .order_by(Complete_Sentence.Id_cs).first()

    return {
        "correct": is_correct,
        "next_id": next_item.Id_cs if next_item else None,
        "next_question": next_item.question_cs if next_item else None
    }


# |----- Listening Sentence Section -----|
# method untuk ambil soal pertama!!
@router.get("/listening-sentence/start/{category_name}")
def start_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return {"error": "Kategori tidak ditemukan"}

    ## ambil soal pertama
    first_question = db.query(Listening_Sentence)\
                       .filter(Listening_Sentence.Id_cat == category.Id_cat)\
                       .order_by(Listening_Sentence.Id_ls).first()

    if first_question:
        return {
            "id_ls": first_question.Id_ls,
            "audio_url": first_question.audio_ls
        }

    return {"error": "Tidak ada soal untuk kategori ini"}

## method untuk ambil soal berikutnya
@router.get("/listening-sentence/{id_ls}/")
def get_question(id_ls: int, db: Session = Depends(get_db)):
    item = db.query(Listening_Sentence).filter(Listening_Sentence.Id_ls == id_ls).first()
    if item:
        return {
            "id_ls": item.Id_ls,
            "audio_url": item.audio_ls,
        }
    
    return {"error": "Soal tidak ditemukan"}

## method untuk pengecekan jawab
@router.post("/listening-sentence/answer/")
async def evaluate_answer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_ls = data.get("id_ls")
    student_answer = data.get("student_answer", "").strip().lower()

    ## cek soal
    question = db.query(Listening_Sentence).filter(Listening_Sentence.Id_ls == id_ls).first()
    if not question:
        return JSONResponse({"error": "Soal tidak ditemukan"}, status_code=404)

    ## ambil full sentence
    reference_sentence = question.sentence_ls.strip().lower()

    ## ambil keywords
    keywords = [k.keyword_answer.strip().lower() for k in question.keywords]

    ## cek nilai similarity model
    emb_ref = similarity_model.encode(reference_sentence, convert_to_tensor=True)
    emb_student = similarity_model.encode(student_answer, convert_to_tensor=True)
    semantic_score = util.pytorch_cos_sim(emb_ref, emb_student).item()

    ## cek nilai keywords
    matched = [k for k in keywords if k in student_answer]
    keyword_score = len(matched) / len(keywords) if keywords else 0
    question_score = round((semantic_score * 0.7) + (keyword_score * 0.3), 2)*100

    current_category_id = question.Id_cat
    next_item = db.query(Listening_Sentence)\
                  .filter(Listening_Sentence.Id_cat == current_category_id, Listening_Sentence.Id_ls > id_ls)\
                  .order_by(Listening_Sentence.Id_ls).first()

    return JSONResponse({
        "question_score": question_score,
        "next_id": next_item.Id_ls if next_item else None,
        "next_audio": next_item.audio_ls if next_item else None
    })

@router.get("/complete-sentence-categories")
def get_complete_sentence_categories(db: Session = Depends(get_db)):
    categories = (
        db.query(Category)
        .join(Complete_Sentence, Category.Id_cat == Complete_Sentence.Id_cat)
        .filter(Complete_Sentence.Id_cat != None)
        .group_by(Category.Id_cat)
        .all()
    )

    return [
        {
            "id": cat.Id_cat,
            "name": cat.name,
            "desc": cat.desc
        }
        for cat in categories
    ]

@router.get("/image-word-categories")
def get_image_word_categories(db: Session = Depends(get_db)):
    categories = (
        db.query(Category)
        .join(Image_Word, Category.Id_cat == Image_Word.Id_cat)
        .filter(Image_Word.Id_cat != None)
        .group_by(Category.Id_cat)
        .all()
    )

    return [
        {
            "id": cat.Id_cat,
            "name": cat.name,
            "desc": cat.desc
        }
        for cat in categories
    ]

@router.get("/listening-word-categories")
def get_listening_word_categories(db: Session = Depends(get_db)):
    categories = (
        db.query(Category)
        .join(Listening_Word, Category.Id_cat == Listening_Word.Id_cat)
        .filter(Listening_Word.Id_cat != None)
        .group_by(Category.Id_cat)
        .all()
    )

    return [
        {
            "id": cat.Id_cat,
            "name": cat.name,
            "desc": cat.desc
        }
        for cat in categories
    ]

@router.get("/listening-sentence-categories")
def get_listening_word_categories(db: Session = Depends(get_db)):
    categories = (
        db.query(Category)
        .join(Listening_Sentence, Category.Id_cat == Listening_Sentence.Id_cat)
        .filter(Listening_Sentence.Id_cat != None)
        .group_by(Category.Id_cat)
        .all()
    )

    return [
        {
            "id": cat.Id_cat,
            "name": cat.name,
            "desc": cat.desc
        }
        for cat in categories
    ]