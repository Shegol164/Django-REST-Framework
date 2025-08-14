from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, LessonViewSet, SubscriptionAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),
]

app_name = 'materials'