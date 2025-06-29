from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

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

class Keyword_Listening(Base):
    __tablename__ = "Keyword_Listening"

    Id_keyword = Column(Integer, primary_key=True, autoincrement=True)
    keyword_answer = Column(String(30))

    Id_ls = Column(Integer, ForeignKey("Listening_Sentence.Id_ls"))
    sentence = relationship("Listening_Sentence", back_populates="keywords")

