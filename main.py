from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# from sentence_transformers import SentenceTransformer, util
from sqlalchemy import func
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base, get_db
from routes import auth_routes, protected
from models import User, Image_Word, Listening_Word, Complete_Sentence, Listening_Sentence, Category, Category, Category, Category, Attempt_Complete_Sentence, Attempt_Listening_Word, Attempt_Listening_Sentence, Attempt_Image_Word, Global_Attempt
from auth import hash_password
from auth import router as auth_router
from datetime import datetime


app = FastAPI()
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

# similarity_model = SentenceTransformer('./models/model')


app.mount("/static", StaticFiles(directory="static"), name="static")

print(hash_password("admin123"))


app.include_router(auth_routes.router)
app.include_router(protected.router)
app.include_router(auth_router)


# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):

#     return templates.TemplateResponse("home.html", {"request": request, "result": None})

# print(hash_password("admin123"))

# @app.get("/listening-word", response_class=None)
# def listening_app(request: Request):
 
#     return templates.TemplateResponse("listening-word/Menu.html", {"request": request})

# @app.get("/listening-word-word", response_class=None)
# def listening_app(request: Request):
 
#     return templates.TemplateResponse("listening-word/listening-word.html", {"request": request})

# @app.get("/complete-sentence", response_class=None)
# def listening_app(request: Request):
 
#     return templates.TemplateResponse("complete-sentence/Menu.html", {"request": request})

# @app.get("/complete-sentence-sentence", response_class=None)
# def listening_app(request: Request):
 
#     return templates.TemplateResponse("complete-sentence/complete-sentence.html", {"request": request})

# @app.get("/listening-sentence", response_class=None)
# def listening_app(request: Request):
 
#     return templates.TemplateResponse("listening-sentence/Menu.html", {"request": request})

# @app.get("/listening-sentence-sentence", response_class=None)
# def listening_app(request: Request):
 
#     return templates.TemplateResponse("listening-sentence/listening-sentence.html", {"request": request})

# @app.get("/image-word", response_class=None)
# def listening_app(request: Request):
 
#     return templates.TemplateResponse("image-word/Menu.html", {"request": request})

# @app.get("/image-word-word", response_class=None)
# def listening_app(request: Request):
 
#     return templates.TemplateResponse("image-word/image-word.html", {"request": request})

# @app.get("/result", response_class=None)
# def listening_app(request: Request):
 
#     return templates.TemplateResponse("score/score.html", {"request": request})


@app.post("/save-attempt")
async def save_attempt(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    print("=== DATA MASUK ===", data)

    features = data.get("feature")
    student_id = data.get("student_id")
    category_name = data.get("category_id")
    score = data.get("score")

    if not student_id or not category_name or score is None:
        return JSONResponse({"error": "Data tidak lengkap"}, status_code=400)

    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return JSONResponse({"error": "Kategori tidak ditemukan"}, status_code=404)
    category_id = category.Id_cat

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

    # Update atau insert skor
    existing_attempt = db.query(tabel).filter(
        tabel.user_id == user.id,
        tabel.Id_cat == category_id
    ).first()

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

    # Update atau insert Global_Attempt
    existing_global = db.query(Global_Attempt).filter(
        Global_Attempt.user_id == user.id,
        Global_Attempt.Id_cat == category_id,
        Global_Attempt.feature_type == features
    ).first()

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

    total_score = db.query(func.sum(Global_Attempt.score)).filter(
        Global_Attempt.user_id == user.id
    ).scalar() or 0

    if user.role == "student" and user.student:
        user.student.total_score = total_score

    db.commit()

    return {"message": "Attempt berhasil disimpan", "score": score}


# !!! INI IMAGE WORD !!!
@app.get("/image-word/start/{category_name}")
def start_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return {"error": "Kategori tidak ditemukan"}

    first_question = db.query(Image_Word)\
                       .filter(Image_Word.Id_cat == category.Id_cat)\
                       .order_by(Image_Word.Id_iw).first()

    if first_question:
        return {
            "id_iw": first_question.Id_iw,
            "image_url": first_question.image_iw
        }

    return {"error": "Tidak ada soal untuk kategori ini"}

@app.get("/image-word/{id_iw}/")
def get_question(id_iw: int, db: Session = Depends(get_db)):
    item = db.query(Image_Word).filter(Image_Word.Id_iw == id_iw).first()
    if item:
        return {
            "id_iw": item.Id_iw,
            "image_url": item.image_iw
        }
    return {"error": "Soal tidak ditemukan"}

@app.post("/image-word/answer/")
async def answer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_iw = data.get("id_iw")
    student_answer = data.get("student_answer", "").strip().lower()

    item = db.query(Image_Word).filter(Image_Word.Id_iw == id_iw).first()
    if not item:
        return JSONResponse({"correct": False, "error": "Soal tidak ditemukan"})

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


# !!! INI LISTENING WORD !!!
@app.get("/listening-word/start/{category_name}")
def start_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return {"error": "Kategori tidak ditemukan"}

    first_question = db.query(Listening_Word)\
                       .filter(Listening_Word.Id_cat == category.Id_cat)\
                       .order_by(Listening_Word.Id_lw).first()

    if first_question:
        return {
            "id_lw": first_question.Id_lw,
            "audio_url": first_question.audio_lw
        }

    return {"error": "Tidak ada soal untuk kategori ini"}

@app.get("/listening-word/{id_lw}/")
def get_question(id_lw: int, db: Session = Depends(get_db)):
    item = db.query(Listening_Word).filter(Listening_Word.Id_lw == id_lw).first()
    if item:
        return {
            "id_lw": item.Id_lw,
            "audio_url": item.audio_lw,
        }
    
    return {"error": "Soal tidak ditemukan"}

@app.post("/listening-word/answer/")
async def answer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_lw = data.get("id_lw")
    student_answer = data.get("student_answer", "").strip().lower()

    item = db.query(Listening_Word).filter(Listening_Word.Id_lw == id_lw).first()
    if not item:
        return JSONResponse({"correct": False, "error": "Soal tidak ditemukan"})

    is_correct = item.lw_answer.strip().lower() == student_answer

    # ambil Id_cat dari soal sekarang
    current_category_id = item.Id_cat

    # ambil soal selanjutnya hanya dalam kategori yang sama
    next_item = db.query(Listening_Word)\
                  .filter(Listening_Word.Id_cat == current_category_id, Listening_Word.Id_lw > id_lw)\
                  .order_by(Listening_Word.Id_lw).first()

    return {
        "correct": is_correct,
        "next_id": next_item.Id_lw if next_item else None,
        "next_audio": next_item.audio_lw if next_item else None
    }


# !!! INI COMPLETE SENTECE !!!
@app.get("/complete-sentence/start/{category_name}")
def start_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return {"error": "Kategori tidak ditemukan"}

    first_question = db.query(Complete_Sentence)\
                       .filter(Complete_Sentence.Id_cat == category.Id_cat)\
                       .order_by(Complete_Sentence.Id_cs).first()

    if first_question:
        return {
            "id_cs": first_question.Id_cs,
            "question": first_question.question_cs
        }

    return {"error": "Tidak ada soal untuk kategori ini"}


@app.get("/complete-sentence/{id_cs}/")
def get_question(id_cs: int, db: Session = Depends(get_db)):
    item = db.query(Complete_Sentence).filter(Complete_Sentence.Id_cs == id_cs).first()
    if item:
        return {
            "id_cs": item.Id_cs,
            "question": item.question_cs
        }
    return {"error": "Soal tidak ditemukan"}


@app.post("/complete-sentence/answer/")
async def answer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_cs = data.get("id_cs")
    student_answer = data.get("student_answer", "").strip().lower()

    item = db.query(Complete_Sentence).filter(Complete_Sentence.Id_cs == id_cs).first()
    if not item:
        return JSONResponse({"correct": False, "error": "Soal tidak ditemukan"})

    is_correct = item.cs_answer.strip().lower() == student_answer

    # ambil Id_cat dari soal sekarang
    current_category_id = item.Id_cat

    # ambil soal selanjutnya hanya dalam kategori yang sama
    next_item = db.query(Complete_Sentence)\
                  .filter(Complete_Sentence.Id_cat == current_category_id, Complete_Sentence.Id_cs > id_cs)\
                  .order_by(Complete_Sentence.Id_cs).first()


    return {
        "correct": is_correct,
        "next_id": next_item.Id_cs if next_item else None,
        "next_question": next_item.question_cs if next_item else None
    }


# !!! INI LISTENING SENTENCE !!!
@app.get("/listening-sentence/start/{category_name}")
def start_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return {"error": "Kategori tidak ditemukan"}

    first_question = db.query(Listening_Sentence)\
                       .filter(Listening_Sentence.Id_cls == category.Id_cls)\
                       .order_by(Listening_Sentence.Id_ls).first()

    if first_question:
        return {
            "id_ls": first_question.Id_ls,
            "audio_url": first_question.audio_ls
        }

    return {"error": "Tidak ada soal untuk kategori ini"}

@app.get("/listening-sentence/{id_ls}/")
def get_question(id_ls: int, db: Session = Depends(get_db)):
    item = db.query(Listening_Sentence).filter(Listening_Sentence.Id_ls == id_ls).first()
    if item:
        return {
            "id_ls": item.Id_ls,
            "audio_url": item.audio_ls,
        }
    
    return {"error": "Soal tidak ditemukan"}

@app.post("/listening-sentence/answer/")
async def evaluate_answer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_ls = data.get("id_ls")
    student_answer = data.get("student_answer", "").strip().lower()

    # Ambil soal sekarang
    question = db.query(Listening_Sentence).filter(Listening_Sentence.Id_ls == id_ls).first()
    if not question:
        return JSONResponse({"error": "Soal tidak ditemukan"}, status_code=404)

    reference_sentence = question.sentence_ls.strip().lower()

    # Ambil keyword dari DB
    keywords = [k.keyword_answer.strip().lower() for k in question.keywords]

    # Similarity score
    emb_ref = similarity_model.encode(reference_sentence, convert_to_tensor=True)
    emb_student = similarity_model.encode(student_answer, convert_to_tensor=True)
    semantic_score = util.pytorch_cos_sim(emb_ref, emb_student).item()

    # Keyword score
    matched = [k for k in keywords if k in student_answer]
    keyword_score = len(matched) / len(keywords) if keywords else 0
    final_score = round((semantic_score * 0.7) + (keyword_score * 0.3), 2)

    # Ambil soal selanjutnya dalam kategori yang sama
    current_category_id = question.Id_cls
    next_item = db.query(Listening_Sentence)\
                  .filter(Listening_Sentence.Id_cls == current_category_id, Listening_Sentence.Id_ls > id_ls)\
                  .order_by(Listening_Sentence.Id_ls).first()

    return JSONResponse({
        "final_score": final_score,
        "next_id": next_item.Id_ls if next_item else None,
        "next_audio": next_item.audio_ls if next_item else None
    })




