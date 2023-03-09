from .base import BaseCommand
from restic_compose_backup import restic


class Command(BaseCommand):
    """List snapshots"""
    name = "snapshots"

    def run(self):
        """Display restic snapshots"""
        stdout, stderr = restic.snapshots(self.config.repository, last=True)
        for line in stdout.decode().split('\n'):
            print(line)
