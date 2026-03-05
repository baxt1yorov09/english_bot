import openai
import whisper
from django.conf import settings
from typing import Dict, List, Optional

class AIScoringService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        try:
            self.whisper_model = whisper.load_model("base")
        except:
            self.whisper_model = None
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file to text using Whisper"""
        try:
            if self.whisper_model:
                result = self.whisper_model.transcribe(audio_file_path)
                return result['text']
            else:
                # Fallback to OpenAI Whisper API
                with open(audio_file_path, 'rb') as audio_file:
                    response = self.openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                    return response.text
        except Exception as e:
            print(f"Audio transcription error: {e}")
            return ""
    
    def evaluate_speaking(self, text: str, question_text: str, part: str) -> Dict:
        """Evaluate speaking response using AI"""
        prompt = f"""
        You are a certified CEFR English examiner. Evaluate the following speaking response.
        
        Question: {question_text}
        Part: {part}
        Response: {text}
        
        Score the response from 0-5 on each criterion:
        - Fluency (smoothness, natural flow)
        - Grammar (accuracy, complexity)
        - Vocabulary (range, appropriateness)
        - Pronunciation (estimated from text patterns)
        - Coherence (organization, linking)
        
        Provide:
        1. Scores for each criterion (0-5)
        2. Overall score (average)
        3. Estimated CEFR level
        4. Specific feedback
        5. List of mistakes
        6. Improved version
        
        Format your response as JSON:
        {{
            "fluency_score": 0.0,
            "grammar_score": 0.0,
            "vocabulary_score": 0.0,
            "pronunciation_score": 0.0,
            "coherence_score": 0.0,
            "overall_score": 0.0,
            "estimated_level": "B1",
            "feedback": "Detailed feedback here",
            "mistakes": ["mistake1", "mistake2"],
            "improved_version": "Improved response here"
        }}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"Speaking evaluation error: {e}")
            return self._get_default_speaking_scores()
    
    def evaluate_writing(self, text: str, question_text: str, task_type: str) -> Dict:
        """Evaluate writing response using AI"""
        word_count = len(text.split())
        
        prompt = f"""
        You are a certified CEFR English examiner. Evaluate the following writing response.
        
        Question: {question_text}
        Task Type: {task_type}
        Word Count: {word_count}
        Response: {text}
        
        Score the response from 0-5 on each criterion:
        - Task Response (addresses all parts of the question)
        - Coherence & Cohesion (organization, linking words)
        - Vocabulary (range, accuracy, collocations)
        - Grammar (range, accuracy, sentence structure)
        
        Provide:
        1. Scores for each criterion (0-5)
        2. Overall score (average)
        3. Estimated CEFR level
        4. Specific feedback
        5. Strengths
        6. Weaknesses
        7. Grammar mistakes
        8. Vocabulary suggestions
        9. Improved version
        
        Format your response as JSON:
        {{
            "task_response_score": 0.0,
            "coherence_score": 0.0,
            "vocabulary_score": 0.0,
            "grammar_score": 0.0,
            "overall_score": 0.0,
            "estimated_level": "B1",
            "feedback": "Detailed feedback here",
            "strengths": ["strength1", "strength2"],
            "weaknesses": ["weakness1", "weakness2"],
            "grammar_mistakes": ["mistake1", "mistake2"],
            "vocabulary_suggestions": ["suggestion1", "suggestion2"],
            "improved_version": "Improved response here"
        }}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
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
