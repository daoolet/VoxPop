from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from datetime import datetime

from repo import CommentsRepo

app = FastAPI()
templates = Jinja2Templates(directory="../template")
repo = CommentsRepo()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/comments")
def get_comments(request: Request):
    comments = repo.get_all()
    context = {
        "request": request,
        "comments": comments
    }
    return templates.TemplateResponse("comments/index.html", context)


@app.get("/comments/new")
def get_new_car(request: Request):
    return templates.TemplateResponse("comments/new.html", {"request": request})


@app.post("/comments/new")
def post_new_comment(
    request: Request,
    text: str = Form(max_length=255),
    category: str = Form()
    ):

    date = datetime.now()

    repo.save(
        {
            "text": text,
            "category": category,
            "date": date,
        }
    )

    print(repo.get_all())
    return RedirectResponse("/comments", status_code = 303)