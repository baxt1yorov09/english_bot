# CEFR English Exam Simulator Telegram Bot

Professional Telegram bot for CEFR speaking and writing exam simulation with AI-powered scoring.

## Features

### Speaking Simulator
- **Part 1** (30 seconds): 3 simple questions
- **Part 1.2** (30 seconds): 2 pictures comparison + questions
- **Part 2** (2 minutes): Situation card discussion
- **Part 3** (2 minutes): Topic discussion with pros/cons

### Writing Simulator
- **Part 1.1** (50+ words): Informal letter to friend
- **Part 1.2** (120+ words): Formal letter to manager
- **Part 2** (180+ words): Academic essay

### AI Features
- Automatic scoring using OpenAI GPT
- Speech-to-text with Whisper
- Grammar and vocabulary analysis
- Personalized feedback

### Admin Dashboard
- User progress tracking
- Performance analytics
- Common mistakes analysis
- Growth charts

### Additional Resources
- Speaking Partner integration
- Reading materials
- Listening practice

## Tech Stack

- **Backend**: Django + DRF
- **Database**: PostgreSQL
- **Cache**: Redis
- **Bot**: aiogram
- **AI**: OpenAI GPT + Whisper
- **Queue**: Celery

## Installation

1. Clone and install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start services:
```bash
# Redis
redis-server

# Celery
celery -A cefr_bot worker -l info

# Django
python manage.py runserver

# Bot
python bot.py
```

## Environment Variables

```
TELEGRAM_BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_django_secret
```

## Project Structure

```
cefr_bot/
├── manage.py
├── requirements.txt
├── bot.py
├── cefr_bot/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/
│   ├── speaking/
│   ├── writing/
│   ├── analytics/
│   └── bot/
└── static/
```

## Usage

1. Start the bot in Telegram
2. Register with your CEFR level
3. Choose speaking or writing practice
4. Complete tasks and get AI feedback
5. Track your progress

## Admin Access

Visit `/admin/` to access the dashboard with:
- User statistics
- Performance analytics
- Content management

## License

MIT License
