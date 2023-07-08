call .venv\Scripts\activate.bat

python .\bin\manage.py makemigrations
python .\bin\manage.py migrate
start /max http://localhost:8000/index/
python .\bin\manage.py runserver