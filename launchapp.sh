python3 -m pip install -r requirements.txt

uvicorn app.main:app --port 8000 --limit-max-requests 20 &

sleep 3

python3 ./app/dashapp.py &

uvicorn_pid=$(ps aux | grep 'uvicorn main:app' | awk '{print $2}')
dash_pid=$(ps aux | grep 'python dash_app.py' | awk '{print $2}')

kill -15 $uvicorn_pid
kill -15 $dash_pid