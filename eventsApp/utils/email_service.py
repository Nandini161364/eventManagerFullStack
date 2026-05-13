from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
import sentry_sdk
from concurrent.futures import ThreadPoolExecutor


email_executor = ThreadPoolExecutor(max_workers=2)


class EmailService:
    @staticmethod
    def _send_mail_async(**kwargs):
        def send():
            try:
                send_mail(**kwargs)
            except Exception as exc:
                sentry_sdk.capture_exception(exc)

        transaction.on_commit(lambda: email_executor.submit(send))

    @staticmethod
    def send_registration_email(user):
        EmailService._send_mail_async(
            subject="Welcome to Event Manager",
            message=(
                f"Hi {user.username},\n\n"
                f"Your account was created successfully."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

    @staticmethod
    def send_booking_confirmation(user):
        EmailService._send_mail_async(
            subject="Booking Confirmed",
            message=(
                f"Hi {user.username},\n\n"
                f"Your booking is confirmed."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
