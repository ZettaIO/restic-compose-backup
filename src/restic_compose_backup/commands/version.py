from .base import BaseCommand


class Command(BaseCommand):
    """Show version"""
    name = "version"

    def run(self):
        import restic_compose_backup
        print(restic_compose_backup.__version__)
