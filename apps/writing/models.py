from django.db import models
from apps.accounts.models import User, CEFRLevel

class WritingQuestion(models.Model):
    TASK_CHOICES = [
        ('1.1', 'Part 1.1 - Informal Letter (50+ words)'),
        ('1.2', 'Part 1.2 - Formal Letter (120+ words)'),
        ('2', 'Part 2 - Essay (180+ words)'),
    ]
    
    task_type = models.CharField(max_length=3, choices=TASK_CHOICES)
    question_text = models.TextField()
    level = models.CharField(max_length=2, choices=CEFRLevel.choices, default=CEFRLevel.B1)
    
    # Sample/Model answer for reference
    sample_answer = models.TextField(blank=True, help_text="Model answer for reference")
    
    # Word count requirements
    min_word_count = models.PositiveIntegerField(default=50)
    max_word_count = models.PositiveIntegerField(default=250)
    
    # Time limit in minutes
    time_limit_minutes = models.PositiveIntegerField(default=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['task_type', 'level']
        
    def __str__(self):
        return f"{self.get_task_type_display()} - {self.question_text[:50]}..."

class WritingAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writing_attempts')
    question = models.ForeignKey(WritingQuestion, on_delete=models.CASCADE)
    
    # User's answer
    answer_text = models.TextField()
    word_count = models.PositiveIntegerField()
    
    # Timing
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    
    # AI Scoring (CEFR Writing Band Descriptors)
    task_response_score = models.FloatField(
        null=True, blank=True, 
        help_text="How well the task was addressed (0-5)"
    )
    coherence_score = models.FloatField(
        null=True, blank=True, 
        help_text="Organization and linking (0-5)"
    )
    vocabulary_score = models.FloatField(
        null=True, blank=True, 
        help_text="Range and accuracy of vocabulary (0-5)"
    )
    grammar_score = models.FloatField(
        null=True, blank=True, 
        help_text="Range and accuracy of grammar (0-5)"
    )
    overall_score = models.FloatField(
        null=True, blank=True, 
        help_text="Overall writing score (0-5)"
    )
    
    # Estimated CEFR band
    estimated_band = models.CharField(
        max_length=2, 
        choices=CEFRLevel.choices, 
        null=True, blank=True
    )
    
    # AI Feedback
    feedback = models.TextField(blank=True)
    strengths = models.TextField(blank=True, help_text="What was done well")
    weaknesses = models.TextField(blank=True, help_text="Areas for improvement")
    grammar_mistakes = models.TextField(blank=True, help_text="List of grammar mistakes")
    vocabulary_suggestions = models.TextField(blank=True, help_text="Better vocabulary alternatives")
    improved_version = models.TextField(blank=True, help_text="AI-improved version")
    
    # Status
    is_completed = models.BooleanField(default=False)
    is_evaluated = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user} - {self.question.get_task_type_display()} ({self.overall_score or 'Pending'})"
    
    def calculate_word_count(self):
        self.word_count = len(self.answer_text.split())
        self.save()
        return self.word_count
    
    def calculate_overall_score(self):
        scores = [
            self.task_response_score,
            self.coherence_score,
            self.vocabulary_score,
            self.grammar_score
        ]
        valid_scores = [s for s in scores if s is not None]
        if valid_scores:
            self.overall_score = sum(valid_scores) / len(valid_scores)
            
            # Estimate CEFR band based on score
            if self.overall_score >= 4.5:
                self.estimated_band = 'C2'
            elif self.overall_score >= 4.0:
                self.estimated_band = 'C1'
            elif self.overall_score >= 3.5:
                self.estimated_band = 'B2'
            elif self.overall_score >= 3.0:
                self.estimated_band = 'B1'
            elif self.overall_score >= 2.5:
                self.estimated_band = 'A2'
            else:
                self.estimated_band = 'A1'
                
            self.save()
        return self.overall_score

class WritingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writing_progress')
    date = models.DateField()
    
    # Daily stats
    total_attempts = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    total_time_minutes = models.PositiveIntegerField(default=0)
    total_words_written = models.PositiveIntegerField(default=0)
    
    # Task-specific averages
    letter_avg = models.FloatField(default=0.0)
    essay_avg = models.FloatField(default=0.0)
    
    # Improvement tracking
    vocabulary_improvement = models.FloatField(default=0.0)
    grammar_improvement = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user} - {self.date} ({self.average_score})"
