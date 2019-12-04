import logging

from restic_compose_backup.alerts.smtp import SMTPAlert
from restic_compose_backup.alerts.discord import DiscordWebhookAlert
from restic_compose_backup.config import Config

logger = logging.getLogger(__name__)

ALERT_INFO = 'INFO',
ALERT_ERROR = 'ERROR'
ALERT_TYPES = [ALERT_INFO, ALERT_ERROR]
BACKENDS = [SMTPAlert, DiscordWebhookAlert]


def configured_alert_classes():
    """Returns a list of configured alert class instances"""
    logger.debug('Getting alert backends')
    entires = []

    for cls in BACKENDS:
        instance = cls.create_from_env()
        logger.debug("Alert backend '%s' configured: %s", cls.name, instance != None)
        if instance:
            entires.append(instance)

    return entires
