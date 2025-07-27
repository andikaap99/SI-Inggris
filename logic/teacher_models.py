from pydantic import BaseModel
from typing import List


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

class LsCreate(BaseModel):
    sentence_ls: str
    audio_ls: str
    keywords: List[str]
    Id_cat: int