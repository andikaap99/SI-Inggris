from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# from sentence_transformers import SentenceTransformer, util
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base
from models import Image_Word

app = FastAPI()
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Model untuk semantic similarity
# similarity_model = SentenceTransformer('./models/model')
# keywords = ['perpustakaan', 'meminjam', 'teman']

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

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

@app.get("/listening/start/")
def start(db: Session = Depends(get_db)):
    first_question = db.query(Image_Word).order_by(Image_Word.Id_iw).first()
    if first_question:
        return {
            "id_iw": first_question.Id_iw,
            "image_url": first_question.image_iw
        }
    return {"error": "Tidak ada soal"}


@app.get("/listening/{id_iw}/")
def get_question(id_iw: int, db: Session = Depends(get_db)):
    item = db.query(Image_Word).filter(Image_Word.Id_iw == id_iw).first()
    if item:
        return {
            "id_iw": item.Id_iw,
            "image_url": item.image_iw
        }
    return {"error": "Soal tidak ditemukan"}


@app.post("/listening/answer/")
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


@app.get("/listening/app/", response_class=None)
def listening_app(request: Request):
    """Render halaman HTML"""
    return templates.TemplateResponse("index.html", {"request": request})