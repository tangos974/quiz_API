python3 -m pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000 &

sleep 3

python3 ./app/dashapp.py

pkill -f "uvicorn main:app"
pkill -f "python dash_app.py"