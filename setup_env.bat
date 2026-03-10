@echo off
REM Use py if available, otherwise python
py -3 -m venv venv || python -m venv venv

REM Activate venv (for CMD)
call .\venv\Scripts\activate.bat

REM Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Virtual environment created and packages installed.
echo Activate it with: .\venv\Scripts\activate.bat
pause
.\setup_env.bat
