from django.db import models
from django.contrib.admin.models import LogEntry
from apps.accounts.models import User

class DailyStats(models.Model):
    date = models.DateField(unique=True)
    
    # User statistics
    total_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    new_users = models.PositiveIntegerField(default=0)
    
    # Practice statistics
    total_speaking_attempts = models.PositiveIntegerField(default=0)
    total_writing_attempts = models.PositiveIntegerField(default=0)
    total_practice_time_minutes = models.PositiveIntegerField(default=0)
    
    # Performance statistics
    avg_speaking_score = models.FloatField(default=0.0)
    avg_writing_score = models.FloatField(default=0.0)
    avg_overall_score = models.FloatField(default=0.0)
    
    # Engagement statistics
    total_messages_sent = models.PositiveIntegerField(default=0)
    total_coins_earned = models.PositiveIntegerField(default=0)
    total_xp_earned = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"Stats for {self.date}"

class UserActivityLog(models.Model):
    ACTION_CHOICES = [
        ('register', 'User Registration'),
        ('speaking_start', 'Speaking Practice Started'),
        ('speaking_complete', 'Speaking Practice Completed'),
        ('writing_start', 'Writing Practice Started'),
        ('writing_complete', 'Writing Practice Completed'),
        ('level_up', 'Level Up'),
        ('streak_achieved', 'Streak Achievement'),
        ('coins_earned', 'Coins Earned'),
        ('login', 'User Login'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    
    # Additional data (JSON format for flexibility)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action', 'created_at']),
        ]
        
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} at {self.created_at}"

class CommonMistake(models.Model):
    SKILL_CHOICES = [
        ('speaking', 'Speaking'),
        ('writing', 'Writing'),
    ]
    
    MISTAKE_TYPE_CHOICES = [
        ('grammar', 'Grammar'),
        ('vocabulary', 'Vocabulary'),
        ('pronunciation', 'Pronunciation'),
        ('fluency', 'Fluency'),
        ('coherence', 'Coherence'),
        ('task_response', 'Task Response'),
    ]
    
    skill = models.CharField(max_length=8, choices=SKILL_CHOICES)
    mistake_type = models.CharField(max_length=15, choices=MISTAKE_TYPE_CHOICES)
    mistake_text = models.CharField(max_length=255)
    
    # Statistics
    frequency = models.PositiveIntegerField(default=0, help_text="How many times this mistake was made")
    affected_users = models.ManyToManyField(User, related_name='common_mistakes')
    
    # AI-generated suggestions
    suggestion = models.TextField(help_text="AI-generated suggestion to fix this mistake")
    example_correction = models.TextField(help_text="Example of correct usage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-frequency']
        unique_together = ['skill', 'mistake_type', 'mistake_text']
        
    def __str__(self):
        return f"{self.skill} - {self.mistake_type}: {self.mistake_text[:50]}..."

class PerformanceReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performance_reports')
    report_date = models.DateField()
    
    # Current performance
    current_level = models.CharField(max_length=2)
    speaking_score = models.FloatField()
    writing_score = models.FloatField()
    overall_score = models.FloatField()
    
    # Progress indicators
    speaking_improvement = models.FloatField(default=0.0, help_text="Change from last period")
    writing_improvement = models.FloatField(default=0.0, help_text="Change from last period")
    overall_improvement = models.FloatField(default=0.0, help_text="Change from last period")
    
    # Time and activity
    total_practice_time = models.PositiveIntegerField(default=0)
    total_attempts = models.PositiveIntegerField(default=0)
    streak_days = models.PositiveIntegerField(default=0)
    
    # AI-generated insights
    strengths = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    next_milestone = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'report_date']
        ordering = ['-report_date']
        
    def __str__(self):
        return f"{self.user} - Report for {self.report_date}"

class SystemMetrics(models.Model):
    date = models.DateField(unique=True)
    
    # System performance
    cpu_usage_avg = models.FloatField(default=0.0, help_text="Average CPU usage %")
    memory_usage_avg = models.FloatField(default=0.0, help_text="Average memory usage %")
    disk_usage = models.FloatField(default=0.0, help_text="Disk usage %")
    
    # Bot performance
    response_time_avg = models.FloatField(default=0.0, help_text="Average bot response time in seconds")
    failed_requests = models.PositiveIntegerField(default=0)
    total_requests = models.PositiveIntegerField(default=0)
    
    # AI usage
    openai_api_calls = models.PositiveIntegerField(default=0)
    openai_tokens_used = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"System Metrics for {self.date}"
