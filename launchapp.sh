python3 -m pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000 &

sleep 5

python3 ./app/dashapp.py