import logging

from allauth.account.signals import email_confirmed
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(email_confirmed)
def activate_user_on_email_confirmed(request, email_address, **kwargs):
    user = email_address.user
    logger.warning('email_confirmed fired: user=%s email=%s', user.pk, email_address.email)
    if not user.is_active:
        user.is_active = True
        user.save(update_fields=['is_active'])