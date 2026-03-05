# CEFR English Exam Simulator - Quick Start Guide

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy environment file
cp .env.example .env

# Edit .env with your API keys:
# TELEGRAM_BOT_TOKEN=your_bot_token_here
# OPENAI_API_KEY=your_openai_key_here
```

### 2. Run the Bot

**Windows:**
```bash
start_bot.bat
```

**Linux/Mac:**
```bash
chmod +x start_bot.sh
./start_bot.sh
```

### 3. Manual Start (if scripts don't work)
```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create sample data
python create_sample_data.py

# Start Django server (terminal 1)
python manage.py runserver

# Start bot (terminal 2)
python run_bot.py
```

## 📱 Bot Features

### Speaking Practice
- **Part 1**: 3 simple questions (30 seconds each)
- **Part 1.2**: Picture comparison (30 seconds)
- **Part 2**: Situation discussion (2 minutes)
- **Part 3**: Topic with pros/cons (2 minutes)

### Writing Practice
- **Part 1.1**: Informal letter to friend (50+ words)
- **Part 1.2**: Formal letter to manager (120+ words)
- **Part 2**: Academic essay (180+ words)

### AI Features
- Automatic scoring (0-5 scale)
- Detailed feedback
- Mistake identification
- Improved version suggestions
- CEFR level estimation

### Additional Resources
- 🎧 Speaking Partner: AI conversation practice
- 📖 Reading: English articles
- 🎙 Listening: Podcasts

## 🎯 Gamification
- XP points for completed tasks
- Coins for rewards
- Daily streak tracking
- Progress monitoring

## 🛠 Admin Dashboard
Visit `http://localhost:8000/admin/` to:
- Monitor user progress
- View analytics
- Manage content
- Track performance

## 📊 API Endpoints

### Writing
- `GET /api/writing/question/?task_type=1.1&level=B1`
- `POST /api/writing/evaluate/`

### Speaking
- `GET /api/speaking/question/?part=1&level=B1`
- `POST /api/speaking/evaluate/`

## 🔧 Configuration

### Required API Keys
1. **Telegram Bot Token**: Get from @BotFather
2. **OpenAI API Key**: Get from platform.openai.com

### Optional
- **Redis URL**: For caching (default: redis://localhost:6379/0)
- **Database URL**: PostgreSQL (default: SQLite)

## 🐛 Troubleshooting

### Common Issues
1. **ModuleNotFoundError**: Install dependencies with `pip install -r requirements.txt`
2. **Bot not responding**: Check TELEGRAM_BOT_TOKEN in .env
3. **AI scoring not working**: Check OPENAI_API_KEY in .env
4. **Database errors**: Run `python manage.py migrate`

### Logs
- Bot logs: Console output
- Django logs: Console output
- Error logs: Check terminal for detailed errors

## 📈 Next Steps

1. **Test the bot**: Send `/start` to your bot
2. **Complete registration**: Set your CEFR level
3. **Try speaking practice**: Record your first response
4. **Practice writing**: Submit your first text
5. **Check progress**: View your statistics

## 🤝 Support

For issues:
1. Check the console logs
2. Verify API keys in .env
3. Ensure all dependencies are installed
4. Check internet connection for AI services

## 📝 Notes

- The bot uses SQLite by default (no setup needed)
- AI scoring requires internet connection
- Audio processing may take 10-30 seconds
- Writing evaluation takes 5-15 seconds
