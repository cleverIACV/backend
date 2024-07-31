from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

#Command execute : python manage.py create_groups
class Command(BaseCommand):
    help = 'Create initial groups'

    def handle(self, *args, **options):
        groups = ['admin', 'recruiter', 'candidate']
        for group in groups:
            Group.objects.get_or_create(name=group)
        self.stdout.write(self.style.SUCCESS('Successfully created initial groups'))