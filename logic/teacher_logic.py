from fastapi import APIRouter, Request, Depends, status, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import engine, Base, get_db
from models import User, Student, Category, Materi, Image_Word, Listening_Word, Complete_Sentence, Listening_Sentence, Category, Category, Keyword_Listening, Category, Category, Attempt_Complete_Sentence, Attempt_Listening_Word, Attempt_Listening_Sentence, Attempt_Image_Word, Global_Attempt
from converter import convert_drive_link, convert_drive_link_pdf
from auth import get_current_user, hash_password
from .teacher_models import *


router = APIRouter()
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


@router.get("/teacher-leaderboard", response_class=JSONResponse)
def leaderboard_home(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    students = (
        db.query(Student)
        .join(User)
        .filter(User.role == "student")
        .order_by(Student.total_score.desc())
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

# Mapping nama fitur ke Model SQLAlchemy dan relasi Category
FEATURE_TABLE_MAPPING = {
    "image-word": Attempt_Image_Word,
    "listening-word": Attempt_Listening_Word,
    "complete-sentence": Attempt_Complete_Sentence,
    "listening-sentence": Attempt_Listening_Sentence
}

FEATURE_TABLE_MAPPING = {
    "image-word": Attempt_Image_Word,
    "listening-word": Attempt_Listening_Word,
    "complete-sentence": Attempt_Complete_Sentence,
    "listening-sentence": Attempt_Listening_Sentence
}

@router.get("/features-leaderboard")
def dynamic_leaderboard(feature: str = Query(...), db: Session = Depends(get_db)):
    AttemptModel = FEATURE_TABLE_MAPPING.get(feature)
    if not AttemptModel:
        raise HTTPException(status_code=400, detail="Fitur tidak valid")

    data = (
        db.query(
            Student.name.label("name"),
            Student.class_name.label("class_name"),
            Category.name.label("category_name"),
            AttemptModel.score.label("score")
        )
        .join(User, User.id == Student.user_id)
        .join(AttemptModel, AttemptModel.user_id == User.id)
        .join(Category, Category.Id_cat == AttemptModel.Id_cat)
        .filter(User.role == "student")
        .order_by(AttemptModel.score.desc())
        .all()
    )

    result = []
    for idx, d in enumerate(data, start=1):
        result.append({
            "no": idx,
            "name": d.name,
            "class_name": d.class_name,
            "category": d.category_name,
            "score": d.score
        })

    return result                                                      

@router.get("/material")
def get_materi(db: Session = Depends(get_db)):
    materials = db.query(Materi).all()
    return [
        {
            "id_mat": material.Id_mat,
            "name": material.name,
            "url": material.url,
            "cat_name": material.category.name
        }
        for material in materials
    ]

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
    materi_link = convert_drive_link_pdf(payload.url)
    try:
        materi = Materi(
            name=payload.name,
            url=materi_link,
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
    audio_link = convert_drive_link(payload.audio_lw)
    try:
        soal = Listening_Word(
            lw_answer=payload.lw_answer,
            audio_lw=audio_link,
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
    
    if payload.get("audio_lw") == question.audio_lw or 'github.com' in payload.get("audio_lw"):
        audio_link = payload.get("audio_lw")
    else:
        audio_link = convert_drive_link(payload.get("audio_lw"))

    question.audio_lw = audio_link
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
    image_link = convert_drive_link(payload.image_iw)

    try:
        soal = Image_Word(
            iw_answer=payload.iw_answer,
            image_iw=image_link,
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
    
    if payload.get("image_iw") == question.image_iw or 'github.com' in payload.get("image_iw"):
        image_link = payload.get("image_iw")
    else:
        image_link = convert_drive_link(payload.get("image_iw"))

    question.iw_answer = payload.get("iw_answer")
    question.image_iw = image_link

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


@router.get("/api/listening-sentence/categories")
def get_ls_categories(db: Session = Depends(get_db)):
    # Ambil hanya kategori yang memiliki listening word
    categories = (
        db.query(Category)
        .join(Listening_Sentence)
        .distinct()
        .all()
    )
    return [{"id_cat": cat.Id_cat, "name": cat.name} for cat in categories]

@router.get("/api/listening-sentence/by-category/{id_cat}")
def get_listening_sentence_by_category(id_cat: int, db: Session = Depends(get_db)):
    soal = (
        db.query(Listening_Sentence)
        .filter(Listening_Sentence.Id_cat == id_cat)
        .all()
    )
    return [
        {
            "id_ls": s.Id_ls,
            "sentence_ls": s.sentence_ls,
            "audio_ls": s.audio_ls,
            "keywords": [k.keyword_answer for k in s.keywords],
            "id_cat": s.Id_cat
        }
        for s in soal
    ]

@router.post("/ls/add", status_code=status.HTTP_200_OK)
def add_materi(payload: LsCreate, db: Session = Depends(get_db)):
    audio_link = convert_drive_link(payload.audio_ls)
    try:
        soal = Listening_Sentence(
            sentence_ls=payload.sentence_ls,
            audio_ls=audio_link,
            Id_cat=payload.Id_cat
        )
        db.add(soal)
        db.flush() 

        for kw in payload.keywords:
            keyword_entry = Keyword_Listening(
                keyword_answer=kw.strip(),
                Id_ls=soal.Id_ls
            )
            db.add(keyword_entry)

        db.commit()

        return {"message": "Soal added successfully"}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        print("ERROR FASTAPI:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/ls/delete")
async def delete_ls(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    soal_id = data.get("soal_id")

    soal = db.query(Listening_Sentence).filter_by(Id_ls=soal_id).first()


    if not soal:
        raise HTTPException(status_code=404, detail="Soal tidak ditemukan.")

    try:
        db.query(Keyword_Listening).filter_by(Id_ls=soal.Id_ls).delete()
        db.delete(soal)
        db.commit()

        return {"message": "Soal berhasil dihapus."}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Terjadi kesalahan saat menghapus materi.")
    
@router.get("/ls/detail/{id_ls}")
def get_cs_detail(id_ls: int, db: Session = Depends(get_db)):
    try:
        print("Masuk endpoint detail:", id_ls)
        question = db.query(Listening_Sentence).filter_by(Id_ls=id_ls).first()

        if not question:
            print("Question tidak ditemukan")
            raise HTTPException(status_code=404, detail="Question not found")

        return {
            "id_ls": question.Id_ls,
            "sentence_ls": question.sentence_ls,
            "audio_ls": question.audio_ls,
            "keywords": [k.keyword_answer for k in question.keywords]
        }
    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/ls/edit")
def edit_question(payload: dict, db: Session = Depends(get_db)):
    question = db.query(Listening_Sentence).filter_by(Id_ls=payload.get("Id_ls")).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if payload.get("audio_ls") == question.audio_ls or 'github.com' in payload.get("audio_ls"):
        audio_link = payload.get("audio_ls")
    else:
        audio_link = convert_drive_link(payload.get("audio_ls"))

    question.audio_ls = audio_link
    question.sentence_ls = payload.get("sentence_ls")
    db.flush() 

    db.query(Keyword_Listening).filter_by(Id_ls=question.Id_ls).delete()

    for kw in payload.get("keywords"):
        keyword_entry = Keyword_Listening(
            keyword_answer=kw.strip(),
            Id_ls=question.Id_ls
        )
        db.add(keyword_entry)

    db.commit()
    return {"message": "Data updated successfully"}
