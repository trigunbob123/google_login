from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'google_id')
    search_fields = ('email', 'username', 'google_id')
    fieldsets = UserAdmin.fieldsets + (
        ('Google 資訊', {'fields': ('google_id', 'profile_image')}),
    )

admin.site.register(User, CustomUserAdmin)