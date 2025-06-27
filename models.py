from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Image_Word(Base):
    __tablename__ = "Image_word"

    Id_iw = Column(Integer, primary_key=True, autoincrement=True)
    iw_answer = Column(String(30))
    image_iw = Column(String(255))


class Listening_Word(Base):
    __tablename__ = "Listening_word"

    Id_lw = Column(Integer, primary_key=True, autoincrement=True)
    lw_answer = Column(String(30))
    audio_lw = Column(String(255))


class Complete_Sentece(Base):
    __tablename__ = "Complete_Sentence"

    Id_cs = Column(Integer, primary_key=True, autoincrement=True)
    question_cs = Column(String(255))
    cs_answer = Column(String(255))


class Listening_Sentence(Base):
    __tablename__ = "Listening_sentence"

    Id_ls = Column(Integer, primary_key=True, autoincrement=True)
    audio_st = Column(String(255))

    # Relasi ke Keyword_Listening (1:N)
    keywords = relationship("Keyword_Listening", back_populates="sentence")


class Keyword_Listening(Base):
    __tablename__ = "Keyword_listening"

    Id_keyword = Column(Integer, primary_key=True, autoincrement=True)
    keyword_answer = Column(String(30))
    Id_ls = Column(Integer, ForeignKey("Listening_sentence.Id_ls"))

    # Relasi balik ke Listening_Sentence
    sentence = relationship("Listening_Sentence", back_populates="keywords")

