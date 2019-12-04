from restic_compose_backup.alerts.base import BaseAlert


class DiscordWebhookAlert(BaseAlert):
    name = 'discord_webhook'

    def __init__(self):
        pass

    @classmethod
    def create_from_env(self):
        return None

    @property
    def properly_configured(self) -> bool:
        return False

    def send(self, subject: str = None, attachment: str = None, alert_type: str = None):
        pass
