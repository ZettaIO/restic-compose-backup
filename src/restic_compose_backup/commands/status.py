from .base import BaseCommand


class Command(BaseCommand):
    """Show status"""
    name = "status"

    def run(self):
        print("Status!")
