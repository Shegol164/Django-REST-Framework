from django.core.management.base import BaseCommand
from celery import current_app

class Command(BaseCommand):
    help = 'Run celery beat'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Celery Beat...'))
        current_app.start(argv=['beat', '-l', 'info', '--scheduler', 'django_celery_beat.schedulers:DatabaseScheduler'])
