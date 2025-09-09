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
        # Создаем группу модераторов
        from django.contrib.auth.models import Group
        moderators_group, created = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(moderators_group)

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
        url = reverse('materials:lesson-list')  # Убедитесь что используете правильное имя URL
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.id,
            'video_link': 'https://www.youtube.com/watch?v=new'
        }
        response = self.client.post(url, data, format='json')

        # Проверяем статус ответа
        print(f"Статус ответа: {response.status_code}")

        # Для диагностики проверяем содержание ответа
        if hasattr(response, 'data'):
            print(f"Данные ответа: {response.data}")
        else:
            print(f"Тип ответа: {type(response)}")
            print(f"Содержание ответа: {response.content}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-detail', args=[self.lesson.id])
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_can_update_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('materials:lesson-detail', args=[self.lesson.id])
        data = {'title': 'Moderator Updated'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('materials:lesson-list')
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.id,
            'video_link': 'https://www.youtube.com/watch?v=new'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.url = reverse('materials:subscriptions')  # Убедитесь в правильности имени URL

    def test_subscribe(self):
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}

        # Подписаться
        response = self.client.post(self.url, data, format='json')

        # Проверяем статус ответа
        print(f"Статус ответа на подписку: {response.status_code}")

        # Для диагностики
        if hasattr(response, 'data'):
            print(f"Данные ответа на подписку: {response.data}")
        else:
            print(f"Тип ответа: {type(response)}")
            print(f"Содержание ответа: {response.content}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем что подписка создалась
        subscription_exists = Subscription.objects.filter(user=self.user, course=self.course).exists()
        print(f"Подписка создана: {subscription_exists}")
        self.assertTrue(subscription_exists)

        # Отписаться
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем что подписка удалилась
        subscription_exists = Subscription.objects.filter(user=self.user, course=self.course).exists()
        print(f"Подписка удалена: {not subscription_exists}")
        self.assertFalse(subscription_exists)