from fastapi import Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from models import User
from auth import role_required


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/homet",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/home.html", {"request": request})

@router.get("/homet-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("teacher"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/question",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/question.html", {"request": request})

@router.get("/question-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("teacher"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/insertls",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/question/menuls.html", {"request": request})

@router.get("/insertls-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("teacher"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/insertlw",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/question/menulw.html", {"request": request})

@router.get("/insertlw-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("teacher"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/insertiw",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/question/menuiw.html", {"request": request})

@router.get("/insertiw-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("teacher"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/insertcs",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/question/menucs.html", {"request": request})

@router.get("/insertcs-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("teacher"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/category",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/category.html", {"request": request})

@router.get("/category-data",response_class=None)
def request(current_user: User = Depends(role_required("teacher"))):

    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/materi",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/materi.html", {"request": request})

@router.get("/materi-data",response_class=None)
def request(current_user: User = Depends(role_required("teacher"))):

    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/student",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/student.html", {"request": request})

@router.get("/student-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("teacher"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/leaderboard",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/leaderboard.html", {"request": request})

@router.get("/leaderboard-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("teacher"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/analysis",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("teacher/analysis.html", {"request": request})

@router.get("/analysis-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("teacher"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}