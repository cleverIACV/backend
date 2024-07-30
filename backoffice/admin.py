from django.contrib import admin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.sessions.models import Session

# Register the models with the admin site if they are not already registered
for model in [Group, User, Permission, Session]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
