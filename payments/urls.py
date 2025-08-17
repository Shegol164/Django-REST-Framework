from django.urls import path
from .views import PaymentAPIView

urlpatterns = [
   path('pay/<int:course_id>/', PaymentAPIView.as_view(), name='payment'),
]