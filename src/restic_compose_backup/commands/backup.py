from .base import BaseCommand


class Command(BaseCommand):
    """Backup a directory"""
    name = "backup"

    def run(self):
        print("Backup!")
