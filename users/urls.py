from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    UserCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserRetrieveUpdateDestroyAPIView.as_view(), name='profile'),
]