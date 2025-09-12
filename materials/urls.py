from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, LessonViewSet, SubscriptionAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

app_name = 'materials'

urlpatterns = [
    path('lessons/', LessonViewSet.as_view({'get': 'list', 'post': 'create'}), name='lesson-list'),
    path('lessons/<int:pk>/', LessonViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='lesson-detail'),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),
]