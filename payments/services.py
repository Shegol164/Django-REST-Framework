import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course_name):
   return stripe.Product.create(name=course_name)

def create_stripe_price(amount, product_id):
   return stripe.Price.create(
      product=product_id,
      unit_amount=int(amount * 100),  # Конвертация в копейки
      currency="rub",
   )


def create_stripe_session(price_id, request):
   domain = request.build_absolute_uri('/')[:-1]  # Получаем базовый URL проекта
   return stripe.checkout.Session.create(
      line_items=[{"price": price_id, "quantity": 1}],
      mode="payment",
      success_url=f"{domain}/payments/success/",  # URL для успешной оплаты
      cancel_url=f"{domain}/payments/cancel/",  # URL для отмены оплаты
   )