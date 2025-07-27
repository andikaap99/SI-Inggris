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
from typing import List
import re
from models import User, Student, Category, Materi, Image_Word, Listening_Word, Complete_Sentence, Listening_Sentence, Category, Category, Keyword_Listening, Category, Category, Attempt_Complete_Sentence, Attempt_Listening_Word, Attempt_Listening_Sentence, Attempt_Image_Word, Global_Attempt
from auth import get_current_user, admin_required
from converter import convert_drive_link, convert_drive_link_pdf












