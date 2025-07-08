from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base

# !!!USER!!!
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)

    student = relationship("Student", uselist=False, back_populates="user")
    teacher = relationship("Teacher", uselist=False, back_populates="user")

    global_attempts = relationship("Global_Attempt", back_populates="user")
    attempts_cs = relationship("Attempt_Complete_Sentences", back_populates="user")
    attempts_iw = relationship("Attempt_Image_Word", back_populates="user")
    attempts_lw = relationship("Attempt_Listening_Word", back_populates="user")
    attempts_ls = relationship("Attempt_Listening_Sentence", back_populates="user")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(50))
    class_name = Column(String(10))
    total_score = Column(Float, default=0)

    user = relationship("User", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(50))

    user = relationship("User", back_populates="teacher")

class Global_Attempt(Base):
    __tablename__ = "Global_Attempt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Menyimpan jenis fitur: 'complete_sentence', 'listening', dll
    feature_type = Column(String(50), nullable=False)

    # Menyimpan ID kategori (bisa untuk join manual ke kategori masing-masing)
    category_id = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="global_attempts")


# !!!IMAGE WORD!!!
class Image_Word(Base):
    __tablename__ = "Image_Word"

    Id_iw = Column(Integer, primary_key=True, autoincrement=True)
    iw_answer = Column(String(30))
    image_iw = Column(String(255))

    Id_ciw = Column(Integer, ForeignKey("Category_Image_Word.Id_ciw"))
    category = relationship("Category_Image_Word", back_populates="question")

class Category_Image_Word(Base):
    __tablename__ = "Category_Image_Word"

    Id_ciw = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))

    question = relationship("Image_Word", back_populates="category")
    attempts = relationship("Attempt_Image_Word", back_populates="category")

class Attempt_Image_Word(Base):
    __tablename__= "Attempt_Image_Word"

    Id_attempt = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float) # Bisa juga pakai Integer jika askornya selalu bulat
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi ke User (pakai user.id)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="attempts_iw")

    # Relasi ke Kategori
    Id_category = Column(Integer, ForeignKey("Category_Image_Word.Id_ciw"))
    category = relationship("Category_Image_Word", back_populates="attempts")

# !!!LISTENING WORD!!!
class Listening_Word(Base):
    __tablename__ = "Listening_Word"

    Id_lw = Column(Integer, primary_key=True, autoincrement=True)
    lw_answer = Column(String(30))
    audio_lw = Column(String(255))

    Id_clw = Column(Integer, ForeignKey("Category_Listening_Word.Id_clw"))
    category = relationship("Category_Listening_Word", back_populates="question")

class Category_Listening_Word(Base):
    __tablename__ = "Category_Listening_Word"

    Id_clw = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))

    question = relationship("Listening_Word", back_populates="category")
    attempts = relationship("Attempt_Listening_Word", back_populates="category")

class Attempt_Listening_Word(Base):
    __tablename__ = "Attempt_Listening_Word"

    Id_attempt = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    #Relasi ke User (pakai user.id)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="attempts_lw")

    #Relasi ke kategori
    Id_category = Column(Integer, ForeignKey("Category_Listening_Word.Id_clw"))
    category = relationship("Category_Listening_Word", back_populates="attempts") 

# !!!COMPLETE SENTENCE!!!
class Complete_Sentence(Base):
    __tablename__ = "Complete_Sentence"

    Id_cs = Column(Integer, primary_key=True, autoincrement=True)
    question_cs = Column(String(255))
    cs_answer = Column(String(255))

    Id_ccs = Column(Integer, ForeignKey("Category_Complete_Sentence.Id_ccs"))
    category = relationship("Category_Complete_Sentence", back_populates="question")

class Category_Complete_Sentence(Base):
    __tablename__ = "Category_Complete_Sentence"

    Id_ccs = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))

    question = relationship("Complete_Sentence", back_populates="category")
    attempts = relationship("Attempt_Complete_Sentences", back_populates="category")

class Attempt_Complete_Sentences(Base):
    __tablename__ = "Attempt_Complete_Sentences"

    Id_attempt = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float)  # Bisa juga pakai Integer jika skornya selalu bulat
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi ke User (pakai user.id)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="attempts_cs")

    # Relasi ke kategori
    Id_category = Column(Integer, ForeignKey("Category_Complete_Sentence.Id_ccs"))
    category = relationship("Category_Complete_Sentence", back_populates="attempts")



class Listening_Sentence(Base):
    __tablename__ = "Listening_Sentence"

    Id_ls = Column(Integer, primary_key=True, autoincrement=True)
    sentence_ls = Column(String(100))
    audio_ls = Column(String(255))

    Id_cls = Column(Integer, ForeignKey("Category_Listening_Sentence.Id_cls"))
    category = relationship("Category_Listening_Sentence", back_populates="question")

    keywords = relationship("Keyword_Listening", back_populates="sentence")

class Category_Listening_Sentence(Base):
    __tablename__ = "Category_Listening_Sentence"

    Id_cls = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))

    question = relationship("Listening_Sentence", back_populates="category")
    attempts = relationship("Attempt_Listening_Sentence", back_populates="category")

class Keyword_Listening(Base):
    __tablename__ = "Keyword_Listening"

    Id_keyword = Column(Integer, primary_key=True, autoincrement=True)
    keyword_answer = Column(String(30))

    Id_ls = Column(Integer, ForeignKey("Listening_Sentence.Id_ls"))
    sentence = relationship("Listening_Sentence", back_populates="keywords")

class Attempt_Listening_Sentence(Base):
    __tablename__ = "Attempt_Listening_Sentence"

    Id_attempt = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi ke User (pakai user.id)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="attempts_ls")

    # Relasi ke kategori
    Id_category = Column(Integer, ForeignKey("Category_Listening_Sentence.Id_cls"))
    category = relationship("Category_Listening_Sentence", back_populates="attempts")

