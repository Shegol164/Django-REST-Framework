from django.core.management.base import BaseCommand
from users.models import Payment, User
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = 'Load sample payment data'

    def handle(self, *args, **options):
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        Payment.objects.create(
            user=user,
            paid_course=course,
            amount=10000,
            payment_method='transfer'
        )

        Payment.objects.create(
            user=user,
            paid_lesson=lesson,
            amount=2000,
            payment_method='cash'
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded payment data'))