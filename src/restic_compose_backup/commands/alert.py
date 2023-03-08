from .base import BaseCommand
from restic_compose_backup import alerts

class Command(BaseCommand):
    """Send an alert"""
    name = "alert"

    def run(self):
        """Test alerts"""
        self.logger.info("Testing alerts")
        containers = self.get_containers()
        alerts.send(
            subject="{}: Test Alert".format(containers.project_name),
            body="Test message",
        )
