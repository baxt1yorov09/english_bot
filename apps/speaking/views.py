from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.speaking.models import SpeakingQuestion, SpeakingAttempt
from apps.accounts.models import User
from apps.bot.ai_service import AIScoringService
import json
from datetime import datetime

@csrf_exempt
def evaluate_speaking(request):
    """API endpoint to evaluate speaking"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            question_id = data.get('question_id')
            user_id = data.get('user_id')
            
            # Get question and user
            question = SpeakingQuestion.objects.get(id=question_id)
            user = User.objects.get(id=user_id)
            
            # Initialize AI service
            ai_service = AIScoringService()
            
            # Evaluate speaking
            result = ai_service.evaluate_speaking(
                text=text,
                question_text=question.question_text,
                part=question.part
            )
            
            # Create speaking attempt
            attempt = SpeakingAttempt.objects.create(
                user=user,
                question=question,
                transcribed_text=text,
                started_at=datetime.now(),
                finished_at=datetime.now(),
                duration_seconds=0,  # Will be updated by frontend
                fluency_score=result.get('fluency_score'),
                grammar_score=result.get('grammar_score'),
                vocabulary_score=result.get('vocabulary_score'),
                pronunciation_score=result.get('pronunciation_score'),
                overall_score=result.get('overall_score'),
                feedback=result.get('feedback'),
                mistakes=result.get('mistakes'),
                improved_version=result.get('improved_version'),
                is_completed=True,
                is_evaluated=True
            )
            
            # Update user stats
            user.speaking_score = result.get('overall_score', 0)
            user.total_score += result.get('overall_score', 0)
            user.add_xp(15)
            user.add_coins(10)
            user.save()
            
            return JsonResponse({
                'success': True,
                'attempt_id': attempt.id,
                'scores': result
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_speaking_question(request):
    """Get a random speaking question"""
    if request.method == 'GET':
        part = request.GET.get('part', '1')
        level = request.GET.get('level', 'B1')
        
        try:
            question = SpeakingQuestion.objects.filter(
                part=part,
                level=level
            ).order_by('?').first()
            
            if question:
                return JsonResponse({
                    'success': True,
                    'question': {
                        'id': question.id,
                        'part': question.part,
                        'question_text': question.question_text,
                        'time_limit': question.time_limit,
                        'picture1_url': question.picture1_url,
                        'picture2_url': question.picture2_url,
                        'pros': question.pros,
                        'cons': question.cons
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No question found'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
