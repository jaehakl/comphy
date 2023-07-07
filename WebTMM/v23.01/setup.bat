rem mkdir %userprofile%\Desktop\Django_server_template
rem cd %userprofile%\Desktop\Django_server_template
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install django djangorestframework django-cors-headers
.\venv\Scripts\python.exe -m pip install pillow django-storages boto3
.\venv\Scripts\python.exe -m pip install dj_rest_auth django-allauth djangorestframework-simplejwt
.\venv\Scripts\python.exe -m pip install numpy

rem .\venv\Scripts\django-admin.exe startproject server
xcopy .\source /e .\bin\

.\venv\Scripts\python.exe .\bin\backend\manage.py makemigrations
.\venv\Scripts\python.exe .\bin\backend\manage.py migrate
.\venv\Scripts\python.exe .\bin\backend\manage.py createsuperuser

start /max http://localhost:8000/index/
.\venv\Scripts\python.exe .\bin\backend\manage.py runserver
pause



