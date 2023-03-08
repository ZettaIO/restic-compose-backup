from .base import BaseCommand


class Command(BaseCommand):
    """Manage crontab"""
    name = "crontab"

    def run(self):
        print("Crontab!")
