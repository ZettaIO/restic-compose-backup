import os
from . import BaseCommand
from restic_compose_backup import restic, alerts, utils

class Command(BaseCommand):
    name = "start_backup_process"

    def run(self):
        """The actual backup process running inside the spawned container"""
        if not utils.is_true(os.environ.get('BACKUP_PROCESS_CONTAINER')):
            self.logger.error(
                "Cannot run backup process in this container. Use backup command instead. "
                "This will spawn a new container with the necessary mounts."
            )
            alerts.send(
                subject="Cannot run backup process in this container",
                body=(
                    "Cannot run backup process in this container. Use backup command instead. "
                    "This will spawn a new container with the necessary mounts."
                )
            )
            exit(1)

        self.run_command("status")  # status(config, containers)
        errors = False
        containers = self.get_containers()

        # Did we actually get any volumes mounted?
        try:
            has_volumes = os.stat('/volumes') is not None
        except FileNotFoundError:
            self.logger.warning("Found no volumes to back up")
            has_volumes = False

        # Warn if there is nothing to do
        if len(containers.containers_for_backup()) == 0 and not has_volumes:
            self.logger.error("No containers for backup found")
            exit(1)

        if has_volumes:
            try:
                self.logger.info('Backing up volumes')
                vol_result = restic.backup_files(self.config.repository, source='/volumes')
                self.logger.debug('Volume backup exit code: %s', vol_result)
                if vol_result != 0:
                    self.logger.error('Volume backup exited with non-zero code: %s', vol_result)
                    errors = True
            except Exception as ex:
                self.logger.error('Exception raised during volume backup')
                self.logger.exception(ex)
                errors = True

        # back up databases
        self.logger.info('Backing up databases')
        for container in containers.containers_for_backup():
            if container.database_backup_enabled:
                try:
                    instance = container.instance
                    self.logger.info('Backing up %s in service %s', instance.container_type, instance.service_name)
                    result = instance.backup()
                    self.logger.debug('Exit code: %s', result)
                    if result != 0:
                        self.logger.error('Backup command exited with non-zero code: %s', result)
                        errors = True
                except Exception as ex:
                    self.logger.exception(ex)
                    errors = True

        if errors:
            self.logger.error('Exit code: %s', errors)
            exit(1)

        # Only run cleanup if backup was successful
        #result = cleanup(config, container)
        self.run_command("cleanup")

        self.logger.debug('cleanup exit code: %s', result)
        if result != 0:
            self.logger.error('cleanup exit code: %s', result)
            exit(1)

        # Test the repository for errors
        self.logger.info("Checking the repository for errors")
        result = restic.check(self.config.repository)
        if result != 0:
            self.logger.error('Check exit code: %s', result)
            exit(1)

        self.logger.info('Backup completed')
