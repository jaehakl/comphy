call set_path.bat

tar -zxvf .\source\python-3.10.11-embed-amd64-pip.tar -C "%cPath%"
xcopy .\source\app .\bin\ /eY

python %PYTHON_DIR%\get-pip.py
python -m pip install --upgrade pip
pip install virtualenv
python -m virtualenv --copies .venv

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install pyside6
pip install numpy matplotlib

python .\bin\main.py
pause