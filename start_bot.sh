#!/bin/bash

echo "Starting CEFR English Exam Simulator Bot..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run Django migrations
echo "Running database migrations..."
python manage.py migrate

# Create sample data
echo "Creating sample data..."
python create_sample_data.py

# Start Django server in background
echo "Starting Django server..."
python manage.py runserver &

# Start the Telegram bot
echo "Starting Telegram bot..."
python run_bot.py
