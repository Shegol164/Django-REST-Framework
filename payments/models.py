from django.conf import settings
from materials.models import Course
from django.db import models


class Payment(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   course = models.ForeignKey(
      'materials.Course',
      on_delete=models.CASCADE,
      related_name='course_payments')
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   stripe_product_id = models.CharField(max_length=100, blank=True)
   stripe_price_id = models.CharField(max_length=100, blank=True)
   stripe_session_id = models.CharField(max_length=100, blank=True)
   payment_link = models.URLField(blank=True)
   is_paid = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)
