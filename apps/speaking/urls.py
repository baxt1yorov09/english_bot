from django.urls import path
from . import views

app_name = 'speaking'

urlpatterns = [
    path('evaluate/', views.evaluate_speaking, name='evaluate_speaking'),
    path('question/', views.get_speaking_question, name='get_speaking_question'),
]
