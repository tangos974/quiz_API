import csv
import random
from fastapi import FastAPI, HTTPException, Request, Query
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

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

# TODO: replace these with requests
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
    return {"question": random_question}


@app.get("/random_filtered_question")
def get_random_filtered(request: Request, use: str = Query(None, title="Use", description="Filter questions by use")):
    """Question Aléatoire filtrée par use
    """
    if use:
        filtered_questions = [q for q in questions_data if q['use'] == use]
        try:
            random_question = random.choice(filtered_questions)
        except IndexError:
            raise HTTPException(
                status_code=404,
                detail='use not in database')
    else:
        random_question = random.choice(questions_data)

    return {"question": random_question}


@app.get("/multiple_responses/")
def read_multiple_responses(request: Request, use: str = Query(None, title="Use", description="Filter questions by use"), num_responses: int = Query(1, ge=1, le=20)):
    """
    """
    if use:
        filtered_questions = [q for q in questions_data if q['use'] == use]
        try:
            selected_questions = random.sample(filtered_questions, min(num_responses, len(filtered_questions)))
        except:
            raise HTTPException(
            status_code=404,
            detail='use not in database')

    else:
        selected_questions = random.sample(questions_data, min(num_responses, len(questions_data)))

    return {"questions": selected_questions}


@app.get("/generate_qcm/")
def generate_qcm(
    request: Request,
    num_questions: int = Query(..., title="Number of Questions", ge=1, le=20),
    use: Optional[str] = Query(None, title="Use", description="Filter questions by use"),
    subjects: Optional[List[str]] = Query(None, title="Subjects", description="Filter questions by subject")
):
    """
    Generate a QCM (Quiz à Choix Multiples) with the specified parameters.
    """
    # Filter questions by use
    filtered_questions = questions_data if use is None else [q for q in questions_data if q['use'] == use]

    # Filter questions by subjects
    if subjects:
        filtered_questions = [q for q in filtered_questions if q['subject'] in subjects]

    # Check if there are enough questions to generate
    if len(filtered_questions) < num_questions:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough questions available for the specified criteria. Total available questions: {len(filtered_questions)}"
        )

    # Select random questions based on the specified criteria
    selected_questions = random.sample(filtered_questions, num_questions)

    return {"qcm": selected_questions}