from django.db import models
from apps.accounts.models import User, CEFRLevel

class SpeakingQuestion(models.Model):
    PART_CHOICES = [
        ('1', 'Part 1 - Introduction'),
        ('1.2', 'Part 1.2 - Picture Description'),
        ('2', 'Part 2 - Situation'),
        ('3', 'Part 3 - Topic Discussion'),
    ]
    
    part = models.CharField(max_length=3, choices=PART_CHOICES)
    question_text = models.TextField()
    level = models.CharField(max_length=2, choices=CEFRLevel.choices, default=CEFRLevel.B1)
    
    # For Part 1.2 - Picture URLs
    picture1_url = models.URLField(null=True, blank=True)
    picture2_url = models.URLField(null=True, blank=True)
    
    # For Part 3 - Pros and Cons
    pros = models.TextField(null=True, blank=True, help_text="Pros for topic discussion")
    cons = models.TextField(null=True, blank=True, help_text="Cons for topic discussion")
    
    # Time limits in seconds
    time_limit = models.PositiveIntegerField(default=30)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['part', 'level']
        
    def __str__(self):
        return f"{self.get_part_display()} - {self.question_text[:50]}..."

class SpeakingAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='speaking_attempts')
    question = models.ForeignKey(SpeakingQuestion, on_delete=models.CASCADE)
    
    # Audio recording
    audio_file = models.FileField(upload_to='speaking/audio/', null=True, blank=True)
    transcribed_text = models.TextField(blank=True)
    
    # Timing
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    duration_seconds = models.PositiveIntegerField()
    
    # AI Scoring
    fluency_score = models.FloatField(null=True, blank=True, help_text="0-5 scale")
    grammar_score = models.FloatField(null=True, blank=True, help_text="0-5 scale")
    vocabulary_score = models.FloatField(null=True, blank=True, help_text="0-5 scale")
    pronunciation_score = models.FloatField(null=True, blank=True, help_text="0-5 scale")
    overall_score = models.FloatField(null=True, blank=True, help_text="0-5 scale")
    
    # AI Feedback
    feedback = models.TextField(blank=True)
    mistakes = models.TextField(blank=True, help_text="List of mistakes found")
    improved_version = models.TextField(blank=True, help_text="AI-improved version")
    
    # Status
    is_completed = models.BooleanField(default=False)
    is_evaluated = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user} - {self.question.get_part_display()} ({self.overall_score or 'Pending'})"
    
    def calculate_overall_score(self):
        scores = [
            self.fluency_score,
            self.grammar_score, 
            self.vocabulary_score,
            self.pronunciation_score
        ]
        valid_scores = [s for s in scores if s is not None]
        if valid_scores:
            self.overall_score = sum(valid_scores) / len(valid_scores)
            self.save()
        return self.overall_score

class SpeakingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='speaking_progress')
    date = models.DateField()
    
    # Daily stats
    total_attempts = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    total_time_minutes = models.PositiveIntegerField(default=0)
    
    # Part-specific averages
    part1_avg = models.FloatField(default=0.0)
    part2_avg = models.FloatField(default=0.0)
    part3_avg = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user} - {self.date} ({self.average_score})"
