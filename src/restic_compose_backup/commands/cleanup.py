from .base import BaseCommand


class Command(BaseCommand):
    """Cleanup old snapshots"""
    name = "cleanup"

    def run(self):
        print("Cleanup!")
