from .base import BaseCommand


class Command(BaseCommand):
    """Send an alert"""
    name = "alert"

    def run(self):
        print("Alert!")
