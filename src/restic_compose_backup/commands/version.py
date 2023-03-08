from .base import BaseCommand


class Command(BaseCommand):
    """Show version"""
    name = "version"

    def run(self):
        print("Version!")
