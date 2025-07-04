from .utils import send_password_reset_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from .models import User
from .utils import send_verification_email


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        user.generate_email_verification_token()
        send_verification_email(user)
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=5)

    def validate(self, data):
        email = data.get('email')
        token = data.get('token')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email.")

        if user.is_email_verified:
            raise serializers.ValidationError("Email is already verified.")

        if user.email_verification_token != token:
            raise serializers.ValidationError("Invalid verification token.")

        if not user.token_created_at or timezone.now() > user.token_created_at + timedelta(minutes=10):
            raise serializers.ValidationError("Token has expired.")

        return data

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.is_email_verified = True
        user.email_verification_token = None
        user.token_created_at = None
        user.save()
        return user


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist.")

        if user.is_email_verified:
            raise serializers.ValidationError("Email is already verified.")

        self.context['user'] = user  # pass user to save method
        return email

    def save(self):
        user = self.context['user']
        user.generate_email_verification_token()
        from .utils import send_verification_email
        send_verification_email(user)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_email_verified:
            raise serializers.ValidationError(
                {"detail": "Please verify your email before logging in."}
            )

        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist.")
        if not user.is_email_verified:
            raise serializers.ValidationError("Email is not verified.")
        self.context['user'] = user
        return email

    def save(self):
        user = self.context['user']
        user.generate_password_reset_token()
        user.save()
        send_password_reset_email(user)
        return user


class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=5)

    def validate(self, data):
        email = data.get('email')
        token = data.get('token')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email.")

        if user.password_reset_token != token:
            raise serializers.ValidationError("Invalid reset token.")

        if not user.password_reset_token_created_at or timezone.now() > user.password_reset_token_created_at + timedelta(minutes=10):
            raise serializers.ValidationError("Token has expired.")

        self.context['user'] = user
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=5)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_token(self, value):
        email = self.initial_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email.")

        if user.password_reset_token != value:
            raise serializers.ValidationError("Invalid reset token.")

        if not user.password_reset_token_created_at or timezone.now() > user.password_reset_token_created_at + timedelta(minutes=10):
            raise serializers.ValidationError("Token has expired.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.set_password(self.validated_data['new_password'])
        user.password_reset_token = None
        user.password_reset_token_created_at = None
        user.save()
        return user
