from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .services import *
from .models import Payment
from materials.models import Course


class PaymentAPIView(APIView):
   def post(self, request, course_id):
      course = get_object_or_404(Course, id=course_id)
      product = create_stripe_product(course.title)
      price = create_stripe_price(course.price, product.id)
      session = create_stripe_session(price.id, request)  # Передаем request

      payment = Payment.objects.create(
         user=request.user,
         course=course,
         amount=course.price,
         stripe_product_id=product.id,
         stripe_price_id=price.id,
         stripe_session_id=session.id,
         payment_link=session.url,
      )

      return Response({"payment_link": session.url}, status=status.HTTP_201_CREATED)
