import urllib.parse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings
import requests
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions
from .serializers import PasswordResetConfirmSerializer, MeSerializer, PasswordResetVerifySerializer, PasswordResetRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, VerifyEmailSerializer, ResendVerificationSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully. Please verify your email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationView(APIView):
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Verification token resent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        if not user.is_email_verified:
            raise AuthenticationFailed("Please verify your email.")

        token, _ = Token.objects.get_or_create(user=user)
        user_data = MeSerializer(user).data

        return Response({
            "token": token.key,
            "user": user_data
        })


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset token sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerifyView(APIView):
    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Token is valid."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(status=204)


class AppleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        identity_token = request.data.get("identity_token")
        email = request.data.get("email")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

        # (Optional) Verify the token with Apple here...

        if not email:
            return Response({"detail": "Email required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Case 1: User already exists → just log them in
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Case 2: Create a new user
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=None

                # password=User.objects.make_random_password()
            )
            user.is_email_verified = True
            user.save()

        # Return or create token
        token, _ = Token.objects.get_or_create(user=user)
        user_data = MeSerializer(user).data

        return Response({
            "token": token.key,
            "user": user_data
        })


# views.py


def facebook_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    # Exchange code for access token
    token_url = "https://graph.facebook.com/v23.0/oauth/access_token"
    params = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": "https://www.ipraymanager.com/accounts/facebook/callback/",
        "client_secret": settings.FACEBOOK_APP_SECRET,
        "code": code,
    }
    resp = requests.get(token_url, params=params).json()

    # This gives you a USER ACCESS TOKEN
    user_access_token = resp.get("access_token")

    # Now fetch page tokens
    page_resp = requests.get(
        f"https://graph.facebook.com/v23.0/me/accounts",
        params={"access_token": user_access_token},
    ).json()

    return JsonResponse(page_resp)


def facebook_login_url(request):
    base_url = "https://www.facebook.com/v23.0/dialog/oauth"
    redirect_uri = "https://www.ipraymanager.com/accounts/facebook/callback/"
    scope = "pages_manage_posts,pages_read_engagement"

    params = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "code",
    }

    auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return JsonResponse({"auth_url": auth_url})


def facebook_page_stats(request):
    page_id = "682008281663366"
    page_token = "EAAzuNAzrstgBPKV75KyFcZCrv4Ox04KPq51ObbzUOW3GZC4LtAR2JPcVHyESqwbi0IjArHOQbylDpA6dbpi3oZBgBlEKCsTwdTuH4dA72fBsx1pWUMPSBIAYTQ7hm3zZBLs269jNrsA9vMnKlFBfOh2YvxCEN9l8aEahzIDIGSk17Jt93K6E4CcZAoKkqUTbK9uZB7witi9ZC82ZAkVk5xkNMvw5"

    url = f"https://graph.facebook.com/v23.0/{page_id}/insights"
    params = {
        "metric": "page_impressions,page_engaged_users,page_fans",
        "access_token": page_token
    }

    resp = requests.get(url, params=params).json()
    return JsonResponse(resp)
