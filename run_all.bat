@echo off
echo Starting MINE Microservices Super App...

cd /d "%~dp0"

echo Activating Virtual Environment...
call venv\Scripts\activate

echo.
echo Starting Main Gateway (Port 8000)...
start "Main Gateway (Port 8000)" cmd /k "call venv\Scripts\activate && cd mine_main && python manage.py runserver 0.0.0.0:8000"

echo Starting Kitchen Service (Port 8001)...
start "Kitchen Service (Port 8001)" cmd /k "call venv\Scripts\activate && cd mine_kitchen && python manage.py runserver 0.0.0.0:8001"

echo Starting Shop Service (Port 8002)...
start "Shop Service (Port 8002)" cmd /k "call venv\Scripts\activate && cd mine_shop && python manage.py runserver 0.0.0.0:8002"

echo Starting Music Service (Port 8003)...
start "Music Service (Port 8003)" cmd /k "call venv\Scripts\activate && cd mine_music && python manage.py runserver 0.0.0.0:8003"

echo.
echo All microservices have been launched in separate windows!
echo.
echo Gateway App: http://192.168.0.106:8000
echo.
pause
