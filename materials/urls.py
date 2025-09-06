from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, LessonViewSet
from materials.views import SubscriptionAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

app_name = 'materials'

urlpatterns = [
    path('', include(router.urls)),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions')
]