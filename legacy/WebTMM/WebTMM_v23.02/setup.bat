set cPath=%cd%
set PYTHON_DIR=%cPath%\python\
set PATH=C:\WINDOWS\system32;C:\WINDOWS;%PYTHON_DIR%;%PYTHON_DIR%\Scripts;

xcopy .\source\python-3.10.11-embed-amd64-pip %PYTHON_DIR% /eY
xcopy .\source\WebTMM .\bin\ /eY

python %PYTHON_DIR%\get-pip.py
pip install --upgrade pip
pip install virtualenv
python -m virtualenv --copies .venv
call .venv\Scripts\activate.bat

pip install django djangorestframework django-cors-headers
pip install pillow django-storages boto3
pip install dj_rest_auth
pip install django-allauth
pip install djangorestframework-simplejwt
pip install numpy

python .\bin\manage.py makemigrations
python .\bin\manage.py migrate
python .\bin\manage.py createsuperuser

start /max http://localhost:8000/index/
python .\bin\manage.py runserver