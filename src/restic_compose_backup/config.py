import os


class Config:
    default_backup_command = ". /env.sh && /backup.sh > /proc/1/fd/1 2>&1"
    default_crontab_schedule = "0 */4 * * *"

    """Bag for config values"""
    def __init__(self, check=True):
        # Mandatory values
        self.repository = os.environ.get('RESTIC_REPOSITORY')
        self.password = os.environ.get('RESTIC_REPOSITORY')
        self.cron_schedule = os.environ.get('CRON_SCHEDULE') or self.default_crontab_schedule
        self.cron_command = os.environ.get('CRON_COMMAND') or self.default_backup_command
        self.swarm_mode = os.environ.get('SWARM_MODE') or False
        self.include_project_name = os.environ.get('INCLUDE_PROJECT_NAME') or False
        self.exclude_bind_mounts = os.environ.get('EXCLUDE_BIND_MOUNTS') or False
        self.skip_cleanup = os.environ.get('SKIP_CLEANUP') or False

        # Log
        self.log_level = os.environ.get('LOG_LEVEL')

        # forget / keep
        self.keep_last = os.environ.get('KEEP_LAST') or "7"
        self.keep_hourly = os.environ.get('KEEP_HOURLY') or "24"
        self.keep_daily = os.environ.get('KEEP_DAILY') or "7"
        self.keep_weekly = os.environ.get('KEEP_WEEKLY') or "4"
        self.keep_monthly = os.environ.get('KEEP_MONTHLY') or "12"
        self.keep_yearly = os.environ.get('KEEP_YEARLY') or "3"
        self.keep_tags = os.environ.get('KEEP_TAGS') or "keep"

        if check:
            self.check()

    def check(self):
        if not self.repository:
            raise ValueError("RESTIC_REPOSITORY env var not set")

        if not self.password:
            raise ValueError("RESTIC_REPOSITORY env var not set")


config = Config()
