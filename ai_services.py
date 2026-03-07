import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import logging
import random
import json
import httpx
from datetime import datetime, timedelta

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cefr_bot.settings')
django.setup()

User = get_user_model()

# Configure logging
logging.basicConfig(level=logging.INFO)

class FreeLLMAIService:
    def __init__(self):
        self.api_key = getattr(settings, 'GROQ_API_KEY', None)
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama3-8b-8192"  # Free Groq model
        logging.info("Free LLM AI Service initialized")
    
    async def _call_groq_api(self, messages, max_tokens=500):
        """Call Groq API for LLM responses"""
        if not self.api_key:
            return None
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    logging.error(f"Groq API error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logging.error(f"Error calling Groq API: {e}")
            return None
    
    async def transcribe_audio(self, audio_file_path):
        """Transcribe audio using simple fallback"""
        return "Voice message received. Audio transcription will be available soon."
    
    async def evaluate_speaking(self, transcript, level, part):
        """Evaluate speaking using free LLM"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a certified CEFR English examiner. Evaluate speaking responses and provide JSON output with scores and feedback.

Return JSON format:
{
    "grammar_score": 4.0,
    "fluency_score": 4.0,
    "vocabulary_score": 4.0,
    "pronunciation_score": 4.0,
    "overall_score": 4.0,
    "feedback": "Detailed feedback here",
    "mistakes": ["mistake1", "mistake2"],
    "improved_version": "Improved response here"
}

Score each criterion from 1.0 to 5.0."""
                },
                {
                    "role": "user",
                    "content": f"""Question: What is your favorite hobby and why?
Level: {level}
Part: {part}
Response: {transcript}

Please evaluate this speaking response."""
                }
            ]
            
            response = await self._call_groq_api(messages)
            
            if response:
                try:
                    # Extract JSON from response
                    import re
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                        return result
                except:
                    pass
            
            # Fallback to simple scoring
            return self._get_fallback_speaking_scores(transcript)
            
        except Exception as e:
            logging.error(f"Error evaluating speaking: {e}")
            return self._get_fallback_speaking_scores(transcript)
    
    async def evaluate_writing(self, text, level, task_type):
        """Evaluate writing using free LLM"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a certified CEFR English examiner. Evaluate writing responses and provide JSON output with scores and feedback.

Return JSON format:
{
    "grammar_score": 4.0,
    "coherence_score": 4.0,
    "vocabulary_score": 4.0,
    "task_achievement_score": 4.0,
    "overall_score": 4.0,
    "feedback": "Detailed feedback here",
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "grammar_mistakes": ["mistake1", "mistake2"],
    "vocabulary_suggestions": ["suggestion1", "suggestion2"],
    "improved_version": "Improved response here"
}

Score each criterion from 1.0 to 5.0."""
                },
                {
                    "role": "user",
                    "content": f"""Task: Write about your favorite hobby
Level: {level}
Task Type: {task_type}
Response: {text}

Please evaluate this writing response."""
                }
            ]
            
            response = await self._call_groq_api(messages)
            
            if response:
                try:
                    # Extract JSON from response
                    import re
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                        return result
                except:
                    pass
            
            # Fallback to simple scoring
            return self._get_fallback_writing_scores(text)
            
        except Exception as e:
            logging.error(f"Error evaluating writing: {e}")
            return self._get_fallback_writing_scores(text)
    
    def _get_fallback_speaking_scores(self, transcript):
        """Fallback speaking evaluation"""
        word_count = len(transcript.split())
        
        # Basic scoring based on response length and complexity
        grammar_score = min(5.0, max(2.0, word_count / 10))
        fluency_score = min(5.0, max(2.0, word_count / 12))
        vocabulary_score = min(5.0, max(2.0, len(set(transcript.lower().split())) / 5))
        pronunciation_score = 4.0  # Default score
        
        overall_score = (grammar_score + fluency_score + vocabulary_score + pronunciation_score) / 4
        
        feedback_parts = []
        if grammar_score >= 3.5:
            feedback_parts.append("Good grammar structure.")
        else:
            feedback_parts.append("Work on grammar accuracy.")
        
        if fluency_score >= 3.5:
            feedback_parts.append("Reasonable fluency.")
        else:
            feedback_parts.append("Practice speaking more fluently.")
        
        if vocabulary_score >= 3.5:
            feedback_parts.append("Decent vocabulary range.")
        else:
            feedback_parts.append("Expand your vocabulary.")
        
        return {
            "grammar_score": grammar_score,
            "fluency_score": fluency_score,
            "vocabulary_score": vocabulary_score,
            "pronunciation_score": pronunciation_score,
            "overall_score": overall_score,
            "feedback": " ".join(feedback_parts),
            "mistakes": ["Some grammar issues", "Limited vocabulary"],
            "improved_version": "This is an improved version with better grammar and vocabulary."
        }
    
    def _get_fallback_writing_scores(self, text):
        """Fallback writing evaluation"""
        word_count = len(text.split())
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        # Basic scoring
        grammar_score = min(5.0, max(2.0, word_count / 15))
        coherence_score = min(5.0, max(2.0, sentences / 3))
        vocabulary_score = min(5.0, max(2.0, len(set(text.lower().split())) / 8))
        task_score = min(5.0, max(2.0, word_count / 20))
        
        overall_score = (grammar_score + coherence_score + vocabulary_score + task_score) / 4
        
        feedback_parts = []
        if grammar_score >= 3.5:
            feedback_parts.append("Strong grammar skills.")
        else:
            feedback_parts.append("Review grammar rules.")
        
        if coherence_score >= 3.5:
            feedback_parts.append("Well-organized text.")
        else:
            feedback_parts.append("Improve text structure.")
        
        if vocabulary_score >= 3.5:
            feedback_parts.append("Good vocabulary usage.")
        else:
            feedback_parts.append("Use more varied vocabulary.")
        
        return {
            "grammar_score": grammar_score,
            "coherence_score": coherence_score,
            "vocabulary_score": vocabulary_score,
            "task_achievement_score": task_score,
            "overall_score": overall_score,
            "feedback": " ".join(feedback_parts),
            "strengths": ["Clear expression", "Good attempt"],
            "weaknesses": ["Minor grammar issues", "Limited vocabulary"],
            "grammar_mistakes": ["Subject-verb agreement", "Article usage"],
            "vocabulary_suggestions": ["Use academic vocabulary", "Try synonyms"],
            "improved_version": "This is an improved version with better grammar and vocabulary."
        }

# Initialize AI service
ai_service = FreeLLMAIService()
