from .base import BaseCommand
from restic_compose_backup import cron

class Command(BaseCommand):
    """Manage crontab"""
    name = "crontab"

    def run(self):
        """Generate the crontab"""
        print(cron.generate_crontab(self.config))
