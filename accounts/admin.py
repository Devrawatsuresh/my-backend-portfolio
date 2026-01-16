# accounts/admin.py
from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
