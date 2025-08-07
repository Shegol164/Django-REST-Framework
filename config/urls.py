from django.urls import path, include
from django.contrib import admin
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Добро пожаловать в API. Используйте /api/ для доступа к ресурсам.")

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('materials.urls', namespace='materials')),
]