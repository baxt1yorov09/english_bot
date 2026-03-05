@echo off
echo Starting CEFR English Exam Simulator Bot...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run Django migrations
echo Running database migrations...
python manage.py migrate

REM Create sample data
echo Creating sample data...
python create_sample_data.py

REM Start Django server in background
echo Starting Django server...
start /B python manage.py runserver

REM Start the Telegram bot
echo Starting Telegram bot...
python run_bot.py

pause
