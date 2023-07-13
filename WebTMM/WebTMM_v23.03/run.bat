call .venv\Scripts\activate.bat

python .\bin\manage.py makemigrations
python .\bin\manage.py migrate
rem start /max http://localhost:8000/index/
start /max .\bin\index.html
python .\bin\manage.py runserver