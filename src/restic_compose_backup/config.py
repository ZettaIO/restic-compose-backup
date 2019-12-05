import os


class Config:
    """Bag for config values"""
    def __init__(self, check=True):
        # Mandatory values
        self.repository = os.environ.get('RESTIC_REPOSITORY')
        self.password = os.environ.get('RESTIC_REPOSITORY')
        self.docker_base_url = os.environ.get('DOCKER_BASE_URL') or "unix://tmp/docker.sock"

        # Log
        self.log_level = os.environ.get('LOG_LEVEL')

        # forget / keep
        self.keep_daily = os.environ.get('KEEP_DAILY') or "7"
        self.keep_weekly = os.environ.get('KEEP_WEEKLY') or "4"
        self.keep_monthly = os.environ.get('KEEP_MONTHLY') or "12"
        self.keep_yearly = os.environ.get('KEEP_YEARLY') or "3"

        if check:
            self.check()

    def check(self):
        if not self.repository:
            raise ValueError("RESTIC_REPOSITORY env var not set")

        if not self.password:
            raise ValueError("RESTIC_REPOSITORY env var not set")