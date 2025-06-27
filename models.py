from sqlalchemy import Column, Integer, String
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
