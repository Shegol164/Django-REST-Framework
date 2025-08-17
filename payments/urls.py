from django.views.generic import TemplateView

urlpatterns = [
    path('pay/<int:course_id>/', PaymentAPIView.as_view(), name='payment'),
    path('success/', TemplateView.as_view(template_name='payments/success.html'), name='payment-success'),
    path('cancel/', TemplateView.as_view(template_name='payments/cancel.html'), name='payment-cancel'),
]