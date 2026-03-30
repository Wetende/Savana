import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_system_email(subject: str, message: str, recipient_list: list[str]) -> int:
    if not recipient_list:
        return 0
    try:
        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    except Exception:
        logger.exception("Failed to send system email to %s", recipient_list)
        return 0
