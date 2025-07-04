from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_email(user):
    subject = "Verify Your Email – IPray Daily"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    context = {
        'name': user.first_name,
        'token': user.email_verification_token,
    }

    html_content = render_to_string("emails/verify_email.html", context)

    msg = EmailMultiAlternatives(subject, '', from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_password_reset_email(user):
    subject = "Reset Your Password – iPrayManager"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    context = {
        "name": user.first_name,
        "token": user.password_reset_token,
    }

    html_content = render_to_string("emails/password_reset.html", context)

    msg = EmailMultiAlternatives(subject, '', from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
