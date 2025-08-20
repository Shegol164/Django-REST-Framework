from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Subscription, Course
from datetime import datetime, timedelta


@shared_task
def send_course_update_notification(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    for sub in subscribers:
        send_mail(
            f'Обновление курса: {course.title}',
            f'Курс "{course.title}" был обновлен. Посмотрите изменения!',
            settings.DEFAULT_FROM_EMAIL,
            [sub.user.email],
            fail_silently=False,
        )