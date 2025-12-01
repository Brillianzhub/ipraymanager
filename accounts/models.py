import random
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_email_verified = models.BooleanField(default=False)

    email_verification_token = models.CharField(
        max_length=5, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)

    password_reset_token = models.CharField(
        max_length=5, blank=True, null=True)
    password_reset_token_created_at = models.DateTimeField(
        blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_allowed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def generate_email_verification_token(self):
        token = str(random.randint(10000, 99999))  # 5-digit
        self.email_verification_token = token
        self.token_created_at = timezone.now()
        self.save()
        return token

    def generate_password_reset_token(self):
        self.password_reset_token = ''.join(
            str(random.randint(0, 9)) for _ in range(5))
        self.password_reset_token_created_at = timezone.now()
        self.save()

    def is_token_valid(self):
        if self.token_created_at is None:
            return False
        return timezone.now() <= self.token_created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
