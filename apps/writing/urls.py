from django.urls import path
from . import views

app_name = 'writing'

urlpatterns = [
    path('evaluate/', views.evaluate_writing, name='evaluate_writing'),
    path('question/', views.get_writing_question, name='get_writing_question'),
]
