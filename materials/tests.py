from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from materials.models import Course, Lesson, Subscription


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='modpass123'
        )
        # Создаем группу модераторов если нужно
        # self.moderator.groups.create(name='moderators')

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            video_link='https://www.youtube.com/watch?v=test',
            owner=self.user
        )

    def test_lesson_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-list')
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.id,
            'video_link': 'https://www.youtube.com/watch?v=new'
        }
        response = self.client.post(url, data, format='json')

        # Вместо print используем assert для проверки статуса
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем что урок создался
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().title, 'New Lesson')

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-detail', args=[self.lesson.id])
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description'
        )

    def test_subscribe(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:subscriptions')
        data = {'course_id': self.course.id}

        # Подписаться
        response = self.client.post(url, data, format='json')

        # Проверяем статус вместо данных
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем что подписка создалась
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Отписаться
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем что подписка удалилась
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())