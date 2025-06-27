from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# from sentence_transformers import SentenceTransformer, util
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base
from models import Image_Word, Listening_Word, Complete_Sentece

app = FastAPI()
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    return templates.TemplateResponse("home.html", {"request": request, "result": None})

@app.get("/listening-word", response_class=None)
def listening_app(request: Request):
 
    return templates.TemplateResponse("listening-word.html", {"request": request})

@app.get("/complete-sentence", response_class=None)
def listening_app(request: Request):
 
    return templates.TemplateResponse("", {"request": request})

@app.get("/listening-sentence", response_class=None)
def listening_app(request: Request):
 
    return templates.TemplateResponse("listening-sentence.html", {"request": request})

@app.get("/image-word", response_class=None)
def listening_app(request: Request):
 
    return templates.TemplateResponse("index.html", {"request": request})


# Model untuk semantic similarity
# similarity_model = SentenceTransformer('./models/model')
# keywords = ['perpustakaan', 'meminjam', 'teman']

# @app.post("/evaluate/")
# async def evaluate(audio_text: str = Form(...), student_summary: str = Form(...)):
    # Similarity Score
    emb_audio = similarity_model.encode(audio_text, convert_to_tensor=True)
    emb_summary = similarity_model.encode(student_summary, convert_to_tensor=True)
    semantic_score = util.pytorch_cos_sim(emb_audio, emb_summary).item()

    # Keyword Score
    matched = [k for k in keywords if k in student_summary.lower()]
    keyword_score = len(matched) / len(keywords)

    # Final Score (gabungan 70% semantic + 30% keyword)
    final_score = (semantic_score * 0.7) + (keyword_score * 0.3)

    return JSONResponse({
        "final_score": round(final_score, 2)
    })



# !!! INI IMAGE WORD !!!
@app.get("/image-word/start/")
def start(db: Session = Depends(get_db)):
    first_question = db.query(Image_Word).order_by(Image_Word.Id_iw).first()
    if first_question:
        return {
            "id_iw": first_question.Id_iw,
            "image_url": first_question.image_iw
        }
    return {"error": "Tidak ada soal"}


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
    next_item = db.query(Image_Word).filter(Image_Word.Id_iw > id_iw).order_by(Image_Word.Id_iw).first()

    return {
        "correct": is_correct,
        "next_id": next_item.Id_iw if next_item else None,
        "next_image": next_item.image_iw if next_item else None
    }


# !!! INI LISTENING WORD !!!
@app.get("/listening-word/start/")
def start(db: Session = Depends(get_db)):
    first_question = db.query(Listening_Word).order_by(Listening_Word.Id_lw).first()
    if first_question:
        return {
            "id_lw": first_question.Id_lw,
            "audio_url": first_question.audio_lw
        }
    return {"error": "Tidak ada soal"}


@app.get("/listening-word/{id_lw}/")
def get_question(id_lw: int, db: Session = Depends(get_db)):
    item = db.query(Listening_Word).filter(Listening_Word.Id_lw == id_lw).first()
    if item:
        return {
            "id_lw": item.Id_lw,
            "audio_url": item.audio_lw
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
    next_item = db.query(Listening_Word).filter(Listening_Word.Id_lw > id_lw).order_by(Listening_Word.Id_lw).first()

    return {
        "correct": is_correct,
        "next_id": next_item.Id_lw if next_item else None,
        "next_audio": next_item.audio_lw if next_item else None
    }


# !!! INI COMPLETE SENTECE !!!
@app.get("/complete-sentence/start/")
def start(db: Session = Depends(get_db)):
    first_question = db.query(Complete_Sentece).order_by(Complete_Sentece.id_cs).first()
    if first_question:
        return {
            "id_cs": first_question.Id_cs,
            "question_cs": first_question.question_cs
        }
    return {"error": "Tidak ada soal"}


@app.get("/complete-sentence/{id_cs}/")
def get_question(id_cs: int, db: Session = Depends(get_db)):
    item = db.query(Complete_Sentece).filter(Complete_Sentece.Id_cs == id_cs).first()
    if item:
        return {
            "id_cs": item.Id_cs,
            "question_cs": item.question_cs
        }
    return {"error": "Soal tidak ditemukan"}


@app.post("/complete-sentence/answer/")
async def answer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_cs = data.get("id_cs")
    student_answer = data.get("student_answer", "").strip().lower()

    item = db.query(Complete_Sentece).filter(Complete_Sentece.Id_cs == id_cs).first()
    if not item:
        return JSONResponse({"correct": False, "error": "Soal tidak ditemukan"})

    is_correct = item.cs_answer.strip().lower() == student_answer
    next_item = db.query(Complete_Sentece).filter(Complete_Sentece.Id_cs > id_cs).order_by(Complete_Sentece.Id_cs).first()

    return {
        "correct": is_correct,
        "next_id": next_item.Id_cs if next_item else None,
        "next_question": next_item.question_cs if next_item else None
    }