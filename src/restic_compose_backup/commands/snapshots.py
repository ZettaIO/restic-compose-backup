from .base import BaseCommand


class Command(BaseCommand):
    """List snapshots"""
    name = "snapshots"

    def run(self):
        print("Snapshots!")
