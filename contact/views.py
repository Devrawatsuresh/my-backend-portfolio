from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from .serializers import ContactSerializer

class ContactAPIView(APIView):
    permission_classes = [AllowAny]  # 👈 important

    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Message sent successfully"},
                status=status.HTTP_201_CREATED
            )

        # ❌ Only return errors if invalid
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
