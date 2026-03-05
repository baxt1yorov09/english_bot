import random
from django.conf import settings
from typing import Dict, List, Optional

class AIScoringService:
    def __init__(self):
        print("Simple AI Service initialized (fallback mode)")
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file to text using simple fallback"""
        return "Voice message received (AI transcription unavailable)"
    
    def evaluate_speaking(self, text: str, question_text: str, part: str) -> Dict:
        """Evaluate speaking response using simple scoring"""
        try:
            # Generate random scores for now
            fluency_score = random.uniform(3.0, 5.0)
            grammar_score = random.uniform(3.0, 5.0)
            vocabulary_score = random.uniform(3.0, 5.0)
            pronunciation_score = random.uniform(3.0, 5.0)
            coherence_score = random.uniform(3.0, 5.0)
            overall_score = (fluency_score + grammar_score + vocabulary_score + pronunciation_score + coherence_score) / 5
            
            # Generate feedback
            feedback_parts = []
            
            if fluency_score >= 4.0:
                feedback_parts.append("Good fluency and natural flow.")
            else:
                feedback_parts.append("Practice speaking more fluently.")
            
            if grammar_score >= 4.0:
                feedback_parts.append("Strong grammar usage.")
            else:
                feedback_parts.append("Work on improving grammar structures.")
            
            if vocabulary_score >= 4.0:
                feedback_parts.append("Rich vocabulary usage.")
            else:
                feedback_parts.append("Expand your vocabulary range.")
            
            if pronunciation_score >= 4.0:
                feedback_parts.append("Clear pronunciation.")
            else:
                feedback_parts.append("Focus on pronunciation clarity.")
            
            if coherence_score >= 4.0:
                feedback_parts.append("Well-organized response.")
            else:
                feedback_parts.append("Improve response organization.")
            
            feedback = " ".join(feedback_parts)
            
            return {
                "fluency_score": fluency_score,
                "grammar_score": grammar_score,
                "vocabulary_score": vocabulary_score,
                "pronunciation_score": pronunciation_score,
                "coherence_score": coherence_score,
                "overall_score": overall_score,
                "estimated_level": "B1",
                "feedback": feedback,
                "mistakes": ["Minor pronunciation issues", "Some grammar gaps"],
                "improved_version": "This is an improved version of your response with better fluency and vocabulary."
            }
        except Exception as e:
            print(f"Speaking evaluation error: {e}")
            return self._get_default_speaking_scores()
    
    def evaluate_writing(self, text: str, question_text: str, task_type: str) -> Dict:
        """Evaluate writing response using simple scoring"""
        word_count = len(text.split())
        
        try:
            # Generate random scores for now
            task_response_score = random.uniform(3.0, 5.0)
            coherence_score = random.uniform(3.0, 5.0)
            vocabulary_score = random.uniform(3.0, 5.0)
            grammar_score = random.uniform(3.0, 5.0)
            overall_score = (task_response_score + coherence_score + vocabulary_score + grammar_score) / 4
            
            # Generate feedback
            feedback_parts = []
            
            if task_response_score >= 4.0:
                feedback_parts.append("Task completed successfully.")
            else:
                feedback_parts.append("Ensure you fully address the task requirements.")
            
            if coherence_score >= 4.0:
                feedback_parts.append("Well-structured and coherent.")
            else:
                feedback_parts.append("Work on text organization and flow.")
            
            if vocabulary_score >= 4.0:
                feedback_parts.append("Diverse vocabulary.")
            else:
                feedback_parts.append("Use more varied vocabulary.")
            
            if grammar_score >= 4.0:
                feedback_parts.append("Strong grammar skills.")
            else:
                feedback_parts.append("Review grammar rules and practice.")
            
            feedback = " ".join(feedback_parts)
            
            return {
                "task_response_score": task_response_score,
                "coherence_score": coherence_score,
                "vocabulary_score": vocabulary_score,
                "grammar_score": grammar_score,
                "overall_score": overall_score,
                "estimated_level": "B1",
                "feedback": feedback,
                "strengths": ["Clear expression", "Good attempt"],
                "weaknesses": ["Minor grammar issues", "Limited vocabulary"],
                "grammar_mistakes": ["Subject-verb agreement", "Article usage"],
                "vocabulary_suggestions": ["Use more academic vocabulary", "Try synonyms"],
                "improved_version": "This is an improved version of your writing with better grammar and vocabulary."
            }
        except Exception as e:
            print(f"Writing evaluation error: {e}")
            return self._get_default_writing_scores()
    
    def _get_default_speaking_scores(self) -> Dict:
        return {
            "fluency_score": 0.0,
            "grammar_score": 0.0,
            "vocabulary_score": 0.0,
            "pronunciation_score": 0.0,
            "coherence_score": 0.0,
            "overall_score": 0.0,
            "estimated_level": "A1",
            "feedback": "Unable to evaluate response. Please try again.",
            "mistakes": [],
            "improved_version": ""
        }
    
    def _get_default_writing_scores(self) -> Dict:
        return {
            "task_response_score": 0.0,
            "coherence_score": 0.0,
            "vocabulary_score": 0.0,
            "grammar_score": 0.0,
            "overall_score": 0.0,
            "estimated_level": "A1",
            "feedback": "Unable to evaluate response. Please try again.",
            "strengths": [],
            "weaknesses": [],
            "grammar_mistakes": [],
            "vocabulary_suggestions": [],
            "improved_version": ""
        }
