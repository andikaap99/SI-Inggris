# routes/protected.py
from fastapi import FastAPI, Request, Form, Depends, Cookie, Query, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth import decode_access_token
from db import SessionLocal, engine, Base
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from jose import JWTError, jwt
from auth import hash_password
from db import get_db
from models import User, Student, Category, Materi, Image_Word, Listening_Word, Complete_Sentence, Listening_Sentence, Category, Category, Keyword_Listening, Category, Category, Attempt_Complete_Sentence, Attempt_Listening_Word, Attempt_Listening_Sentence, Attempt_Image_Word, Global_Attempt
from auth import get_current_user, admin_required


class QuestionBase(BaseModel):
    feature: str
    category: str
    question: str = ""
    answer: str = ""
    image_url: str = ""
    audio_url: str = ""
    keyword: str = ""

class QuestionInsert(QuestionBase):
    pass

class QuestionEditDelete(QuestionBase):
    id: int

class StudentCreate(BaseModel):
    name: str
    username: str
    class_name: str
    hashed_password: str

class CategoryCreate(BaseModel):
    category: str
    desc: str

class MateriCreate(BaseModel):
    name: str
    url: str
    category: int

class CsCreate(BaseModel):
    question_cs: str
    cs_answer: str
    Id_cat: int

class LwCreate(BaseModel):
    lw_answer: str
    audio_lw: str
    Id_cat: int

class IwCreate(BaseModel):
    iw_answer: str
    image_iw: str
    Id_cat: int


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/home", response_class=HTMLResponse)
async def read_root(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("home2.html", {"request": request, "result": None})

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

@router.get("/profile", response_class=HTMLResponse)
async def read_root(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("profile.html", {"request": request, "result": None})

@router.get("/profile-global-attempts")
def get_user_global_attempts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # pakai dict, bukan User
):
    user = db.query(User).filter(User.username == current_user["username"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Ambil semua global attempt milik user ini
    attempts = db.query(Global_Attempt).filter(Global_Attempt.user_id == user.id).all()

    results = []
    for a in attempts:
        # Cari nama kategori sesuai tipe fitur
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

@router.get("/listening-word", response_class=None)
def listening_word(request: Request, current_user: User = Depends(get_current_user)):
 
    return templates.TemplateResponse("listening-word/Menu.html", {"request": request})

@router.get("/listening-word-word", response_class=None)
def listening_word(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("listening-word/listening-word.html", {"request": request})

@router.get("/listening-sentence",response_class=None)
def listening_sentence(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("listening-sentence/Menu.html", {"request": request})


@router.get("/listening-sentence-sentence",response_class=None)
def listening_sentence(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("listening-sentence/listening-sentence.html", {"request": request})


@router.get("/complete-sentence",response_class=None)
def complete_sentence(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("complete-sentence/Menu.html", {"request": request})


@router.get("/complete-sentence-sentence",response_class=None)
def complete_sentence_sentence(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("complete-sentence/complete-sentence.html", {"request": request})

@router.get("/image-word",response_class=None)
def image_word(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("image-word/Menu.html", {"request": request})

@router.get("/image-word-word",response_class=None)
def image_word(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("image-word/image-word.html", {"request": request})

@router.get("/result",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("score/score.html", {"request": request})

@router.get("/homet",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/home.html", {"request": request})

@router.get("/question",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/question.html", {"request": request})

@router.get("/insertls",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/question/menuls.html", {"request": request})

@router.get("/insertlw",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/question/menulw.html", {"request": request})

@router.get("/insertiw",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/question/menuiw.html", {"request": request})

@router.get("/insertcs",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/question/menucs.html", {"request": request})

@router.get("/insert-question",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("insert_question.html", {"request": request})

@router.get("/edit-question",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("edit_question.html", {"request": request})

@router.get("/delete-question",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("delete_question.html", {"request": request})

@router.get("/category",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/category.html", {"request": request})

@router.get("/materi",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/materi.html", {"request": request})

@router.get("/student",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/student.html", {"request": request})

@router.get("/leaderboard",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/leaderboard.html", {"request": request})

@router.get("/analysis",response_class=None)
def request(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse("teacher/analysis.html", {"request": request})


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

                                                               

@router.post("/questions/add")
def add_question(payload: dict, db: Session = Depends(get_db)):
    feature = payload.get("feature")
    category = payload.get("category")

    if not feature or not category:
        raise HTTPException(status_code=400, detail="Feature dan category wajib diisi.")

    try:
        if feature == "image-word":
            cat = db.query(Category).filter_by(name=category).first()
            if not cat:
                raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")
            soal = Image_Word(
                iw_answer=payload.get("answer"),
                image_iw=payload.get("image_url"),
                Id_ciw=cat.Id_ciw
            )
            db.add(soal)

        elif feature == "listening-word":
            cat = db.query(Category).filter_by(name=category).first()
            if not cat:
                raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")
            soal = Listening_Word(
                lw_answer=payload.get("answer"),
                audio_lw=payload.get("audio_url"),
                Id_clw=cat.Id_clw
            )
            db.add(soal)

        elif feature == "complete-sentence":
            cat = db.query(Category).filter_by(name=category).first()
            if not cat:
                raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")
            soal = Complete_Sentence(
                question_cs=payload.get("question"),
                cs_answer=payload.get("answer"),
                Id_ccs=cat.Id_ccs
            )
            db.add(soal)

        elif feature == "listening-sentence":
            cat = db.query(Category).filter_by(name=category).first()
            if not cat:
                raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")
            soal = Listening_Sentence(
                sentence_ls=payload.get("answer"),  # answer = full kalimat
                audio_ls=payload.get("audio_url"),
                Id_cls=cat.Id_cls
            )
            db.add(soal)
            db.flush()  # agar Id_ls muncul sebelum commit

            # Simpan keyword (dipisah koma)
            keywords = payload.get("keyword", "").split(",")
            for kw in keywords:
                kw_clean = kw.strip()
                if kw_clean:
                    keyword_obj = Keyword_Listening(
                        keyword=kw_clean,
                        Id_ls=soal.Id_ls
                    )
                    db.add(keyword_obj)

        else:
            raise HTTPException(status_code=400, detail="Fitur tidak dikenali.")

        db.commit()
        return {"message": f"Soal berhasil ditambahkan ke fitur {feature}."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")
    

@router.get("/questions/list")
def get_questions_list(feature: str = Query(...), category: str = Query(...), db: Session = Depends(get_db)):
    result = []

    if feature == "image-word":
        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")
        questions = db.query(Image_Word).filter_by(Id_ciw=cat.Id_ciw).all()
        result = [{"id": q.Id_iw, "preview": q.iw_answer} for q in questions]

    elif feature == "listening-word":
        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")
        questions = db.query(Listening_Word).filter_by(Id_clw=cat.Id_clw).all()
        result = [{"id": q.Id_lw, "preview": q.lw_answer} for q in questions]

    elif feature == "complete-sentence":
        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")
        questions = db.query(Complete_Sentence).filter_by(Id_ccs=cat.Id_ccs).all()
        result = [{"id": q.Id_cs, "preview": q.question_cs} for q in questions]

    elif feature == "listening-sentence":
        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")
        questions = db.query(Listening_Sentence).filter_by(Id_cls=cat.Id_cls).all()
        result = [{"id": q.Id_ls, "preview": q.sentence_ls} for q in questions]

    else:
        raise HTTPException(status_code=400, detail="Invalid feature")

    return result


@router.get("/questions/detail")
def get_question_detail(
    feature: str = Query(..., description="Fitur soal, misalnya: 'complete-sentence'"),
    id: int = Query(..., description="ID soal yang ingin diambil"),
    db: Session = Depends(get_db)
):
    if feature == "complete-sentence":
        question = db.query(Complete_Sentence).filter_by(Id_cs=id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan")
        return {
            "question": question.question_cs,
            "answer": question.cs_answer
        }

    elif feature == "listening-sentence":
        question = db.query(Listening_Sentence).filter_by(Id_ls=id).first()

        if not question:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan")

        return {
            "question": question.sentence_ls,
            "audio_url": question.audio_ls,
            "keyword": ", ".join([kw.keyword_answer for kw in question.keywords])
        }

    elif feature == "listening-word":
        question = db.query(Listening_Word).filter_by(Id_lw=id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan")
        return {
            "audio_url": question.audio_lw,
            "answer": question.lw_answer
        }

    elif feature == "image-word":
        question = db.query(Image_Word).filter_by(Id_iw=id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan")
        return {
            "image_url": question.image_iw,
            "answer": question.iw_answer
        }

    else:
        raise HTTPException(status_code=400, detail="Fitur tidak valid")
    

@router.post("/questions/edit")
def edit_question(data: QuestionEditDelete, db: Session = Depends(get_db)):
    feature = data.feature
    category = data.category

    if not feature or not category:
        raise HTTPException(status_code=400, detail="Feature dan kategori wajib diisi.")

    # === 1. Complete Sentence ===
    if feature == "complete-sentence":
        soal = db.query(Complete_Sentence).filter_by(Id_cs=data.id).first()
        if not soal:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")

        soal.question_cs = data.question
        soal.cs_answer = data.answer
        soal.Id_ccs = cat.Id_ccs

    # === 2. Listening Word ===
    elif feature == "listening-word":
        soal = db.query(Listening_Word).filter_by(Id_lw=data.id).first()
        if not soal:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")

        soal.lw_answer = data.answer
        soal.audio_lw = data.audio_url
        soal.Id_clw = cat.Id_clw

    # === 3. Image Word ===
    elif feature == "image-word":
        soal = db.query(Image_Word).filter_by(Id_iw=data.id).first()
        if not soal:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")

        soal.iw_answer = data.answer
        soal.image_iw = data.image_url
        soal.Id_ciw = cat.Id_ciw

    # === 4. Listening Sentence ===
    elif feature == "listening-sentence":
        soal = db.query(Listening_Sentence).filter_by(Id_ls=data.id).first()
        if not soal:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")

        soal.sentence_ls = data.answer
        soal.audio_ls = data.audio_url
        soal.Id_cls = cat.Id_cls

        # Hapus keyword lama
        db.query(Keyword_Listening).filter_by(Id_ls=soal.Id_ls).delete()

        # Tambahkan keyword baru
        if data.keyword:
            keyword_list = [k.strip() for k in data.keyword.split(",") if k.strip()]
            for k in keyword_list:
                db.add(Keyword_Listening(Id_ls=soal.Id_ls, keyword_answer=k))

    else:
        raise HTTPException(status_code=400, detail="Fitur tidak dikenali.")

    db.commit()
    return {"message": "Soal berhasil diperbarui."}


@router.post("/questions/delete")
def delete_question(data: QuestionEditDelete, db: Session = Depends(get_db)):
    feature = data.feature
    category = data.category

    if not feature or not category:
        raise HTTPException(status_code=400, detail="Feature dan kategori wajib diisi.")

    # === 1. Complete Sentence ===
    if feature == "complete-sentence":
        soal = db.query(Complete_Sentence).filter_by(Id_cs=data.id).first()
        if not soal:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")

        db.delete(soal)

    # === 2. Listening Word ===
    elif feature == "listening-word":
        soal = db.query(Listening_Word).filter_by(Id_lw=data.id).first()
        if not soal:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")

        db.delete(soal)

    # === 3. Image Word ===
    elif feature == "image-word":
        soal = db.query(Image_Word).filter_by(Id_iw=data.id).first()
        if not soal:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")

        db.delete(soal)

    # === 4. Listening Sentence ===
    elif feature == "listening-sentence":
        soal = db.query(Listening_Sentence).filter_by(Id_ls=data.id).first()
        if not soal:
            raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

        cat = db.query(Category).filter_by(name=category).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")

        db.delete(soal)

        # Hapus keyword lama
        db.query(Keyword_Listening).filter_by(Id_ls=soal.Id_ls).delete()

    else:
        raise HTTPException(status_code=400, detail="Fitur tidak dikenali.")

    db.commit()
    return {"message": "Soal berhasil dihapus."}


@router.get("/api/students")
def get_students(db: Session = Depends(get_db)):
    results = (
        db.query(
            Student.name,
            User.username,
            Student.class_name,
            User.id.label("user_id")
        )
        .join(User)
        .all()
    )

    return [
        {
            "name": r.name,
            "username": r.username,
            "class_name": r.class_name,
            "user_id": r.user_id
        }
        for r in results
    ]

@router.post("/student/add")
def add_student(payload: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(username=payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        user = User(
            username=payload.username,
            hashed_password=hash_password(payload.hashed_password),
            role="student"  # huruf kecil!
        )
        db.add(user)
        db.flush()  # agar user.id terbentuk

        student = Student(
            user_id=user.id,
            name=payload.name,
            class_name=payload.class_name,
            total_score=0
        )
        db.add(student)
        db.commit()

        return {"message": "Student and User added successfully"}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()  # penting! agar kamu tahu kesalahannya
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/students/detail/{user_id}")
def get_student_detail(user_id: int, db: Session = Depends(get_db)):
    try:
        print("Masuk endpoint detail:", user_id)
        student = db.query(Student).filter_by(user_id=user_id).first()

        if not student:
            print("Student tidak ditemukan")
            raise HTTPException(status_code=404, detail="Student not found")

        user = student.user
        if not user:
            print("User relasi tidak ditemukan untuk student.user_id:", student.user_id)
            raise HTTPException(status_code=404, detail="Related user not found")

        print("Berhasil ambil data:", student.name, user.username)

        return {
            "user_id": student.user_id,
            "name": student.name,
            "class_name": student.class_name,
            "username": user.username,
            "hashed_password": ""
        }
    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.post("/student/edit")
def edit_student(payload: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    student = db.query(Student).filter_by(user_id=user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update user
    user.username = payload.get("username")
    if payload.get("hashed_password") == "":
        pass
    else:
        user.hashed_password = hash_password(payload.get("hashed_password"))

    # Update student
    student.name = payload.get("name")
    student.class_name = payload.get("class_name")

    db.commit()
    return {"message": "Student and User updated successfully"}

@router.post("/student/delete")
async def delete_student(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id wajib disertakan.")

    student = db.query(Student).filter_by(user_id=user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan.")

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")
    
    # ✅ Hapus dulu data attempt yang berkaitan
    db.query(Global_Attempt).filter_by(user_id=user_id).delete()

    db.delete(student)
    db.delete(user)
    db.commit()

    return {"message": "Siswa dan user berhasil dihapus."}


@router.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return [
        {
            "id_cat": category.Id_cat,
            "name": category.name,
            "desc": category.desc
        }
        for category in categories
    ]

@router.post("/category/add")
def add_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    try:
        category = Category(
            name=payload.category,
            desc=payload.desc
        )
        db.add(category)
        db.flush()

        db.commit()

        return {"message": "Category added successfully"}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/category/delete")
async def delete_category(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    category_id = data.get("category_id")

    if not category_id:
        raise HTTPException(status_code=400, detail="category_id wajib disertakan.")

    category = db.query(Category).filter_by(Id_cat=category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan.")

    try:
        # Hapus data attempt (urutan penting)
        db.query(Attempt_Image_Word).filter_by(Id_cat=category_id).delete()
        db.query(Attempt_Listening_Word).filter_by(Id_cat=category_id).delete()
        db.query(Attempt_Complete_Sentence).filter_by(Id_cat=category_id).delete()
        db.query(Attempt_Listening_Sentence).filter_by(Id_cat=category_id).delete()

        # Hapus Listening_Sentence dan Keywordnya
        ls_items = db.query(Listening_Sentence).filter_by(Id_cat=category_id).all()
        for ls in ls_items:
            db.query(Keyword_Listening).filter_by(Id_ls=ls.Id_ls).delete()
        db.query(Listening_Sentence).filter_by(Id_cat=category_id).delete()

        # Hapus soal-soal lain
        db.query(Image_Word).filter_by(Id_cat=category_id).delete()
        db.query(Listening_Word).filter_by(Id_cat=category_id).delete()
        db.query(Complete_Sentence).filter_by(Id_cat=category_id).delete()

        # Hapus Global_Attempt yang terkait dengan kategori ini
        db.query(Global_Attempt).filter_by(Id_cat=category_id).delete()

        # Hapus kategori
        db.delete(category)
        db.commit()

        return {"message": "Kategori dan semua data terkait berhasil dihapus."}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Terjadi kesalahan saat menghapus kategori.")
    

@router.get("/api/materi")
def get_materi(db: Session = Depends(get_db)):
    materi = db.query(Materi).all()
    return [
        {
            "id_mat": m.Id_mat,
            "name": m.name,
            "url": m.url,
            "id_cat": m.Id_cat
        }
        for m in materi
    ]

@router.post("/materi/add")
def add_materi(payload: MateriCreate, db: Session = Depends(get_db)):
    try:
        materi = Materi(
            name=payload.name,
            url=payload.url,
            Id_cat=payload.category
        )
        db.add(materi)
        db.flush()

        db.commit()

        return {"message": "Materi added successfully"}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/materi/delete")
async def delete_materi(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    materi_id = data.get("materi_id")

    materi = db.query(Materi).filter_by(Id_mat=materi_id).first()

    if not materi:
        raise HTTPException(status_code=404, detail="Materi tidak ditemukan.")

    try:
        # Hapus kategori
        db.delete(materi)
        db.commit()

        return {"message": "Materi berhasil dihapus."}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Terjadi kesalahan saat menghapus materi.")
    

@router.get("/api/listening-word/categories")
def get_lw_categories(db: Session = Depends(get_db)):
    # Ambil hanya kategori yang memiliki listening word
    categories = (
        db.query(Category)
        .join(Listening_Word)
        .distinct()
        .all()
    )
    return [{"id_cat": cat.Id_cat, "name": cat.name} for cat in categories]

@router.get("/api/listening-word/by-category/{id_cat}")
def get_listening_words_by_category(id_cat: int, db: Session = Depends(get_db)):
    soal = (
        db.query(Listening_Word)
        .filter(Listening_Word.Id_cat == id_cat)
        .all()
    )
    return [
        {
            "id_lw": s.Id_lw,
            "answer": s.lw_answer,
            "audio": s.audio_lw,
            "id_cat": s.Id_cat
        }
        for s in soal
    ]

@router.post("/lw/add", status_code=status.HTTP_200_OK)
def add_materi(payload: LwCreate, db: Session = Depends(get_db)):
    try:
        soal = Listening_Word(
            lw_answer=payload.lw_answer,
            audio_lw=payload.audio_lw,
            Id_cat=payload.Id_cat
        )
        db.add(soal)
        db.flush()
        db.commit()

        return {"message": "Soal added successfully"}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        print("ERROR FASTAPI:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/lw/delete")
async def delete_cs(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    soal_id = data.get("soal_id")

    soal = db.query(Listening_Word).filter_by(Id_lw=soal_id).first()

    if not soal:
        raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

    try:
        # Hapus kategori
        db.delete(soal)
        db.commit()

        return {"message": "Soal berhasil dihapus."}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Terjadi kesalahan saat menghapus materi.")
    
@router.get("/lw/detail/{id_lw}")
def get_cs_detail(id_lw: int, db: Session = Depends(get_db)):
    try:
        print("Masuk endpoint detail:", id_lw)
        question = db.query(Listening_Word).filter_by(Id_lw=id_lw).first()

        if not question:
            print("Question tidak ditemukan")
            raise HTTPException(status_code=404, detail="Question not found")

        return {
            "id_lw": question.Id_lw,
            "audio_lw": question.audio_lw,
            "lw_answer": question.lw_answer,
            "id_cat": question.Id_cat
        }
    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/lw/edit")
def edit_question(payload: dict, db: Session = Depends(get_db)):
    question = db.query(Listening_Word).filter_by(Id_lw=payload.get("Id_lw")).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    question.audio_lw = payload.get("audio_lw")
    question.lw_answer = payload.get("lw_answer")

    db.commit()
    return {"message": "Data updated successfully"}


@router.get("/api/image-word/categories")
def get_iw_categories(db: Session = Depends(get_db)):
    # Ambil hanya kategori yang memiliki listening word
    categories = (
        db.query(Category)
        .join(Image_Word)
        .distinct()
        .all()
    )
    return [{"id_cat": cat.Id_cat, "name": cat.name} for cat in categories]

@router.get("/api/image-word/by-category/{id_cat}")
def get_image_words_by_category(id_cat: int, db: Session = Depends(get_db)):
    soal = (
        db.query(Image_Word)
        .filter(Image_Word.Id_cat == id_cat)
        .all()
    )
    return [
        {
            "id_iw": s.Id_iw,
            "iw_answer": s.iw_answer,
            "image_iw": s.image_iw,
            "id_cat": s.Id_cat
        }
        for s in soal
    ]

@router.post("/iw/add", status_code=status.HTTP_200_OK)
def add_materi(payload: IwCreate, db: Session = Depends(get_db)):
    try:
        soal = Image_Word(
            iw_answer=payload.iw_answer,
            image_iw=payload.image_iw,
            Id_cat=payload.Id_cat
        )
        db.add(soal)
        db.flush()
        db.commit()

        return {"message": "Soal added successfully"}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        print("ERROR FASTAPI:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/iw/delete")
async def delete_cs(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    soal_id = data.get("soal_id")

    soal = db.query(Image_Word).filter_by(Id_iw=soal_id).first()

    if not soal:
        raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

    try:
        # Hapus kategori
        db.delete(soal)
        db.commit()

        return {"message": "Soal berhasil dihapus."}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Terjadi kesalahan saat menghapus materi.")

@router.get("/iw/detail/{id_iw}")
def get_cs_detail(id_iw: int, db: Session = Depends(get_db)):
    try:
        print("Masuk endpoint detail:", id_iw)
        question = db.query(Image_Word).filter_by(Id_iw=id_iw).first()

        if not question:
            print("Question tidak ditemukan")
            raise HTTPException(status_code=404, detail="Question not found")

        return {
            "id_iw": question.Id_iw,
            "iw_answer": question.iw_answer,
            "image_iw": question.image_iw,
            "id_cat": question.Id_cat
        }
    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/iw/edit")
def edit_question(payload: dict, db: Session = Depends(get_db)):
    question = db.query(Image_Word).filter_by(Id_iw=payload.get("Id_iw")).first()
    if not question:
        raise HTTPException(status_code=404, detail="Data not found")

    question.iw_answer = payload.get("iw_answer")
    question.image_iw = payload.get("image_iw")

    db.commit()
    return {"message": "Data updated successfully"}


@router.get("/api/complete-sentence/categories")
def get_cs_categories(db: Session = Depends(get_db)):
    # Ambil hanya kategori yang memiliki listening word
    categories = (
        db.query(Category)
        .join(Complete_Sentence)
        .distinct()
        .all()
    )
    return [{"id_cat": cat.Id_cat, "name": cat.name} for cat in categories]

@router.get("/api/complete-sentence/by-category/{id_cat}")
def get_complete_sentence_by_category(id_cat: int, db: Session = Depends(get_db)):
    soal = (
        db.query(Complete_Sentence)
        .filter(Complete_Sentence.Id_cat == id_cat)
        .all()
    )
    return [
        {
            "id_cs": s.Id_cs,
            "cs_answer": s.cs_answer,
            "question_cs": s.question_cs,
            "id_cat": s.Id_cat
        }
        for s in soal
    ]

@router.post("/cs/add", status_code=status.HTTP_200_OK)
def add_materi(payload: CsCreate, db: Session = Depends(get_db)):
    try:
        soal = Complete_Sentence(
            question_cs=payload.question_cs,
            cs_answer=payload.cs_answer,
            Id_cat=payload.Id_cat
        )
        db.add(soal)
        db.flush()
        db.commit()

        return {"message": "Soal added successfully"}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        print("ERROR FASTAPI:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cs/delete")
async def delete_cs(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    soal_id = data.get("soal_id")

    soal = db.query(Complete_Sentence).filter_by(Id_cs=soal_id).first()

    if not soal:
        raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

    try:
        # Hapus kategori
        db.delete(soal)
        db.commit()

        return {"message": "Soal berhasil dihapus."}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Terjadi kesalahan saat menghapus materi.")

@router.get("/cs/detail/{id_cs}")
def get_cs_detail(id_cs: int, db: Session = Depends(get_db)):
    try:
        print("Masuk endpoint detail:", id_cs)
        question = db.query(Complete_Sentence).filter_by(Id_cs=id_cs).first()

        if not question:
            print("Question tidak ditemukan")
            raise HTTPException(status_code=404, detail="Question not found")

        return {
            "id_cs": question.Id_cs,
            "question_cs": question.question_cs,
            "cs_answer": question.cs_answer,
            "id_cat": question.Id_cat
        }
    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/cs/edit")
def edit_question(payload: dict, db: Session = Depends(get_db)):
    question = db.query(Complete_Sentence).filter_by(Id_cs=payload.get("Id_cs")).first()
    if not question:
        raise HTTPException(status_code=404, detail="User not found")

    question.question_cs = payload.get("question_cs")
    question.cs_answer = payload.get("cs_answer")

    db.commit()
    return {"message": "Student and User updated successfully"}
