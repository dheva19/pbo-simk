from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'role', 'is_staff')
    
    search_fields = ('full_name', 'username', 'email')
    list_filter = ('role',)