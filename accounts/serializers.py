from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


# -----------------------------
# Register Serializer
# -----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "full_name",
            "phone_number",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


# -----------------------------
# Login Serializer
# -----------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["email"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data["user"] = user
        return data


# -----------------------------
# Profile Serializer
# -----------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "full_name",
            "phone_number",
            "profile_image",
            "role",
        )
