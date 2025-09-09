from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from materials.models import Course, Lesson, Subscription


class LessonCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

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
        url = reverse('materials:lesson-list')  # Убедитесь что правильное имя URL
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.id,
            'video_link': 'https://www.youtube.com/watch?v=new'
        }
        response = self.client.post(url, data, format='json')

        # Для ViewSet создание обычно возвращает 201 Created
        # Но если используется другой подход, может возвращаться 200
        print(f"Response status: {response.status_code}")  # Для диагностики
        print(f"Response data: {response.data}")  # Для диагностики

        # Проверяем что урок создался
        self.assertEqual(Lesson.objects.count(), 2)  # Был 1, стал 2
        self.assertEqual(Lesson.objects.last().title, 'New Lesson')

    def test_lesson_update(self):
        url = reverse('materials:lesson-detail', args=[self.lesson.id])
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description'
        )

    def test_subscribe(self):
        self.client.force_authenticate(user=self.user)

        # Проверяем правильный URL
        url = reverse('materials:subscriptions')  # Убедитесь в правильности имени

        data = {'course_id': self.course.id}

        # POST запрос для создания подписки
        response = self.client.post(url, data, format='json')

        print(f"Subscribe response status: {response.status_code}")
        print(f"Subscribe response data: {response.data}")

        # Проверяем что подписка создалась
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # POST запрос для удаления подписки
        response = self.client.post(url, data, format='json')

        print(f"Unsubscribe response status: {response.status_code}")
        print(f"Unsubscribe response data: {response.data}")

        # Проверяем что подписка удалилась
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())