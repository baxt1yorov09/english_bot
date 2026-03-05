from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta

class CEFRLevel(models.TextChoices):
    A1 = 'A1', 'A1 (Beginner)'
    A2 = 'A2', 'A2 (Elementary)'
    B1 = 'B1', 'B1 (Intermediate)'
    B2 = 'B2', 'B2 (Upper Intermediate)'
    C1 = 'C1', 'C1 (Advanced)'
    C2 = 'C2', 'C2 (Proficient)'

class User(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True)
    
    # CEFR Information
    current_level = models.CharField(
        max_length=2, 
        choices=CEFRLevel.choices, 
        default=CEFRLevel.A1
    )
    target_level = models.CharField(
        max_length=2, 
        choices=CEFRLevel.choices, 
        default=CEFRLevel.B1
    )
    
    # Profile Information
    full_name = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    daily_goal = models.PositiveIntegerField(default=30, help_text="Minutes per day")
    
    # Statistics
    total_score = models.PositiveIntegerField(default=0)
    speaking_score = models.FloatField(default=0.0, help_text="Average speaking score")
    writing_score = models.FloatField(default=0.0, help_text="Average writing score")
    total_practice_time = models.PositiveIntegerField(default=0, help_text="Total practice minutes")
    
    # Gamification
    coins = models.PositiveIntegerField(default=0)
    xp = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0, help_text="Daily practice streak")
    last_practice_date = models.DateField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"@{self.telegram_username or self.username} ({self.current_level})"
    
    def update_streak(self):
        from datetime import date
        today = date.today()
        
        if self.last_practice_date == today:
            return  # Already practiced today
        
        if self.last_practice_date == today - timedelta(days=1):
            self.streak += 1
        else:
            self.streak = 1
            
        self.last_practice_date = today
        self.save()
    
    def add_xp(self, amount):
        self.xp += amount
        self.save()
        
    def add_coins(self, amount):
        self.coins += amount
        self.save()
