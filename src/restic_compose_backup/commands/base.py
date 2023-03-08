from restic_compose_backup.config import Config


class BaseCommand:
    """Base class for all commands"""
    name = "base"

    def __init__(self):
        self.config = Config()
    
    def run(self):
        raise NotImplementedError
