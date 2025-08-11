from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

app_name = 'materials'

urlpatterns = [
    path('', include(router.urls)),
]