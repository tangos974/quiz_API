import csv
import random
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount le dossier 'static' qui contiendra les fichiers statiques: css, images, javascript
app.mount("/static", StaticFiles(directory="static"), name="static")

# Charge les données depuis le fichier csv
questions_data = []
with open("questions.csv", newline="", encoding="utf-8") as csvfile:
    csvreader = csv.DictReader(csvfile)
    questions_data = list(csv.DictReader(csvfile))


class Question(BaseModel):
    """Une question du tableau
    """
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: Optional[str] = None
    responseD: Optional[str] = None
    remark: Optional[str] = None



@app.get('/')
def get_index():
    """Message de Bienvenue
    """
    return{'message': 'Bienvenue sur mon API'}

@app.get("/random_question")
def get_random(request: Request):
    """Question Aléatoire
    """
    random_question = random.choice(questions_data)
    return templates.TemplateResponse("index.html", {"request": request, "question": random_question})