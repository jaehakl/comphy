.\venv\Scripts\python.exe .\bin\backend\manage.py makemigrations
.\venv\Scripts\python.exe .\bin\backend\manage.py migrate
start /max http://localhost:8000/index/
.\venv\Scripts\python.exe .\bin\backend\manage.py runserver
pause
