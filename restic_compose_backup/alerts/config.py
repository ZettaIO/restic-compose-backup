"""Check config and expose properly configured alert backends"""
from restic_compose_backup.alerts.smtp import SMTPAlert
from restic_compose_backup.alerts.discord import DiscordWebhookAlert
from restic_compose_backup.config import Config


BACKENDS = [SMTPAlert, DiscordWebhookAlert]


def configured_alert_classes():
    """Returns a list of configured alert class instances"""
    config = Config()
    entires = []

    for cls in BACKENDS:
        instance = cls.create_from_config(config)
        if instance:
            entires.append(instance)

    return entires
