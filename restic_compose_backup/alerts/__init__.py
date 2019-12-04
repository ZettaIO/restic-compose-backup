from restic_compose_backup.alerts.smtp import SMTPAlert
from restic_compose_backup.alerts.discord import DiscordWebhookAlert
from restic_compose_backup.config import Config

ALERT_INFO = 'INFO',
ALERT_ERROR = 'ERROR'
ALERT_TYPES = [ALERT_INFO, ALERT_ERROR]
BACKENDS = [SMTPAlert, DiscordWebhookAlert]


def send(subject: str = None, attachment: str = None, alert_type: str = ALERT_ERROR):
    """Send an alert"""
    pass


def configured_alert_classes():
    """Returns a list of configured alert class instances"""
    entires = []

    for cls in BACKENDS:
        instance = cls.create_from_env()
        if instance:
            entires.append(instance)

    return entires
