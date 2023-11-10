import csv
import random
from fastapi import FastAPI, Request, Query
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

#TODO: replace these with requests
possible_subjects = set(q['subject'] for q in questions_data)
possible_uses = set(q['use'] for q in questions_data)

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
    return templates.TemplateResponse("random_question.html", {"request": request, "question": random_question})

@app.get("/random_filtered_question")
def get_random_filtered(request: Request, use: str = Query(None, title="Use", description="Filter questions by use")):
    """Question Aléatoire
    """
    if use:
        filtered_questions = [q for q in questions_data if q['use'] == use]
        random_question = random.choice(filtered_questions)
    else:
        random_question = random.choice(questions_data)

    return templates.TemplateResponse("random_filtered_question.html", {"request": request, "question": random_question, "uses": possible_uses})