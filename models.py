from sqlalchemy import Column, Integer, String
from db import Base

class Image_Word(Base):
    __tablename__ = "Image_word"

    Id_iw = Column(Integer, primary_key=True, autoincrement=True)
    iw_answer = Column(String(255))
    image_iw = Column(String(255))
