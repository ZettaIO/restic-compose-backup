from .base import BaseCommand


class Command(BaseCommand):
    """Test a command"""
    name = "test"

    def run(self):
        print("Test!")
