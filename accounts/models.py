from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import os
import uuid


# -----------------------------
# Profile Image Upload Path
# -----------------------------
def user_profile_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("users", str(instance.id), filename)


# -----------------------------
# Custom User Manager
# -----------------------------
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", CustomUser.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# -----------------------------
# Custom User Model
# -----------------------------
class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        CUSTOMER = "CUSTOMER", _("Customer")

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to=user_profile_upload_path,
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """
        Rules:
        - Superuser is ALWAYS ADMIN
        - ADMIN has staff access
        - CUSTOMER has no staff/superuser access
        """

        if self.is_superuser:
            self.role = self.Role.ADMIN
            self.is_staff = True

        elif self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = False

        else:
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.role})"
