from .base import BaseCommand
from restic_compose_backup import restic


class Command(BaseCommand):
    """Cleanup old snapshots"""
    name = "cleanup"

    def run(self):
        """Run forget / prune to minimize storage space"""
        self.logger.info('Forget outdated snapshots')
        forget_result = restic.forget(
            self.config.repository,
            self.config.keep_daily,
            self.config.keep_weekly,
            self.config.keep_monthly,
            self.config.keep_yearly,
        )
        self.logger.info('Prune stale data freeing storage space')
        prune_result = restic.prune(self.config.repository)
        return forget_result and prune_result
