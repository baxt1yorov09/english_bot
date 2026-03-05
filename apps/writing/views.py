from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from apps.writing.models import WritingQuestion, WritingAttempt
from apps.accounts.models import User
from apps.bot.ai_service import AIScoringService
import json
from datetime import datetime

@csrf_exempt
def evaluate_writing(request):
    """API endpoint to evaluate writing"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            question_id = data.get('question_id')
            user_id = data.get('user_id')
            
            # Get question and user
            question = WritingQuestion.objects.get(id=question_id)
            user = User.objects.get(id=user_id)
            
            # Initialize AI service
            ai_service = AIScoringService()
            
            # Evaluate writing
            result = ai_service.evaluate_writing(
                text=text,
                question_text=question.question_text,
                task_type=question.task_type
            )
            
            # Create writing attempt
            attempt = WritingAttempt.objects.create(
                user=user,
                question=question,
                answer_text=text,
                word_count=len(text.split()),
                started_at=datetime.now(),
                finished_at=datetime.now(),
                duration_minutes=0,  # Will be updated by frontend
                task_response_score=result.get('task_response_score'),
                coherence_score=result.get('coherence_score'),
                vocabulary_score=result.get('vocabulary_score'),
                grammar_score=result.get('grammar_score'),
                overall_score=result.get('overall_score'),
                estimated_band=result.get('estimated_level'),
                feedback=result.get('feedback'),
                strengths='\n'.join(result.get('strengths', [])),
                weaknesses='\n'.join(result.get('weaknesses', [])),
                grammar_mistakes='\n'.join(result.get('grammar_mistakes', [])),
                vocabulary_suggestions='\n'.join(result.get('vocabulary_suggestions', [])),
                improved_version=result.get('improved_version'),
                is_completed=True,
                is_evaluated=True
            )
            
            # Update user stats
            user.writing_score = result.get('overall_score', 0)
            user.total_score += result.get('overall_score', 0)
            user.add_xp(10)
            user.add_coins(5)
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
def get_writing_question(request):
    """Get a random writing question"""
    if request.method == 'GET':
        task_type = request.GET.get('task_type', '1.1')
        level = request.GET.get('level', 'B1')
        
        try:
            question = WritingQuestion.objects.filter(
                task_type=task_type,
                level=level
            ).order_by('?').first()
            
            if question:
                return JsonResponse({
                    'success': True,
                    'question': {
                        'id': question.id,
                        'task_type': question.task_type,
                        'question_text': question.question_text,
                        'min_word_count': question.min_word_count,
                        'max_word_count': question.max_word_count,
                        'time_limit_minutes': question.time_limit_minutes,
                        'sample_answer': question.sample_answer
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
