from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags


def send_activation_email(email, email_token):
    subject = "Your account needs to verified"
    email_from = settings.EMAIL_HOST_USER
    # message = (
    #     f"Hey, you just created an account so you need to verify that account. "
    #     f"Click on the link below to verify your account: http://127.0.0.1:8000/account/activate/{email_token}"
    # )
    message = f"Click on the link below to verify your account: http://127.0.0.1:8000/account/activate/{email_token}/"

    #Create the plain text version of the email (needed for some email clients)
    # plain_message = strip_tags(message)

    send_mail(
        subject,
        # plain_message,
        message,  # Pass the HTML message for email clients that support HTML
        email_from,
        [email],
    )

def send_password_reset_email(email, reset_password_token):
    subject = "Password Reset Request"
    email_from = settings.EMAIL_HOST_USER
    message = (
        "Hey, you just requested a password reset. " 
        f"Click on the link below to reset your password: http://127.0.0.1:8000/account/password/reset/{reset_password_token}/"
    )
    send_mail(
        subject,
        message,  # Pass the HTML message for email clients that support HTML
        email_from,
        [email],
    )