from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db import SessionLocal, engine
from models import User, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/")
def read_users(request: Request, db: Session = Depends(get_db)):
    """Mengambil semua user dari tabel user dan render dengan HTML"""
    users = db.query(User).all()
    return templates.TemplateResponse("index.html", {"request": request, "users": users})
