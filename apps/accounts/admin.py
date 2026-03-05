from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CEFRLevel

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('telegram_username', 'full_name', 'current_level', 'target_level', 'total_score', 'coins', 'streak', 'created_at')
    list_filter = ('current_level', 'target_level', 'created_at', 'is_active')
    search_fields = ('telegram_username', 'full_name', 'email')
    ordering = ('-created_at',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('CEFR Information', {
            'fields': ('telegram_id', 'telegram_username', 'current_level', 'target_level', 'full_name', 'age', 'daily_goal')
        }),
        ('Statistics', {
            'fields': ('total_score', 'speaking_score', 'writing_score', 'total_practice_time')
        }),
        ('Gamification', {
            'fields': ('coins', 'xp', 'streak', 'last_practice_date')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('CEFR Information', {
            'fields': ('telegram_id', 'telegram_username', 'current_level', 'target_level')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'total_practice_time')
