from fastapi import Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from models import User
from auth import role_required


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/home")
def home_page(request: Request):
    return templates.TemplateResponse("home2.html", {"request": request})

@router.get("/home-data")
def home_data(current_user: dict = Depends(role_required("student"))):
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/profile", response_class=HTMLResponse)
async def read_root(request: Request):

    return templates.TemplateResponse("profile.html", {"request": request, "result": None})

@router.get("/profile-data")
def home_data(current_user: dict = Depends(role_required("student"))):

    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/learn")
def home_page(request: Request):

    return templates.TemplateResponse("learning/learn.html", {"request": request})

@router.get("/learn-data")
def home_data(current_user: dict = Depends(role_required("student"))):

    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/listening-word")
def home_page(request: Request):
    
    return templates.TemplateResponse("listening-word/Menu.html", {"request": request})

@router.get("/listening-word-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("student"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/listening-word-word", response_class=None)
def listening_word(request: Request):

    return templates.TemplateResponse("listening-word/listening-word.html", {"request": request})

@router.get("/listening-word-word-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("student"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/listening-sentence",response_class=None)
def listening_sentence(request: Request):

    return templates.TemplateResponse("listening-sentence/Menu.html", {"request": request})

@router.get("/listening-sentence-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("student"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/listening-sentence-sentence",response_class=None)
def listening_sentence(request: Request):

    return templates.TemplateResponse("listening-sentence/listening-sentence.html", {"request": request})

@router.get("/listening-sentence-sentence-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("student"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}


@router.get("/complete-sentence",response_class=None)
def complete_sentence(request: Request):

    return templates.TemplateResponse("complete-sentence/Menu.html", {"request": request})

@router.get("/complete-sentence-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("student"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/complete-sentence-sentence",response_class=None)
def complete_sentence_sentence(request: Request):

    return templates.TemplateResponse("complete-sentence/complete-sentence.html", {"request": request})

@router.get("/complete-sentence-sentence-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("student"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/image-word",response_class=None)
def image_word(request: Request):

    return templates.TemplateResponse("image-word/Menu.html", {"request": request})

@router.get("/image-word-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("student"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/image-word-word",response_class=None)
def image_word(request: Request):

    return templates.TemplateResponse("image-word/image-word.html", {"request": request})

@router.get("/image-word-word-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("student"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/result",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("score/score.html", {"request": request})

@router.get("/result-data", response_class=None)
def listening_word(request: Request, current_user: User = Depends(role_required("student"))):
 
    return {"message": "This is protected data", "user": current_user["username"]}

@router.get("/result-ls",response_class=None)
def request(request: Request):

    return templates.TemplateResponse("score/score_ls.html", {"request": request})

@router.get("/result-ls-data",response_class=None)
def request(current_user: User = Depends(role_required("student"))):

    return {"message": "This is protected data", "user": current_user["username"]}