from django.contrib import admin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.sessions.models import Session
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register the models with the admin site if they are not already registered
for model in [Group, User, Permission, Session]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

# Save constum User
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'date_joined', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)