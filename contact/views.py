# contact/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .serializers import ContactSerializer

class ContactAPIView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
