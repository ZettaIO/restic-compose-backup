from .base import BaseCommand
from restic_compose_backup import utils, restic


class Command(BaseCommand):
    """Show status"""
    name = "status"

    def run(self):
        """Outputs the backup config for the compose setup"""
        containers = self.get_containers()

        self.logger.info("Status for compose project '%s'", containers.project_name)
        self.logger.info("Repository: '%s'", self.config.repository)
        self.logger.info("Backup currently running?: %s", containers.backup_process_running)
        self.logger.info("Include project name in backup path?: %s", utils.is_true(self.config.include_project_name))
        self.logger.debug("Exclude bind mounts from backups?: %s", utils.is_true(self.config.exclude_bind_mounts))
        self.logger.info("Checking docker availability")

        utils.list_containers()

        if containers.stale_backup_process_containers:
            utils.remove_containers(containers.stale_backup_process_containers)

        # Check if repository is initialized with restic snapshots
        if not restic.is_initialized(self.config.repository):
            self.logger.info("Could not get repository info. Attempting to initialize it.")
            result = restic.init_repo(self.config.repository)
            if result == 0:
                self.logger.info("Successfully initialized repository: %s", self.config.repository)
            else:
                self.logger.error("Failed to initialize repository")

        self.logger.info("%s Detected Config %s", "-" * 25, "-" * 25)

        # Start making snapshots
        backup_containers = containers.containers_for_backup()
        for container in backup_containers:
            self.logger.info('service: %s', container.service_name)

            if container.volume_backup_enabled:
                for mount in container.filter_mounts():
                    self.logger.info(
                        ' - volume: %s -> %s',
                        mount.source,
                        container.get_volume_backup_destination(mount, '/volumes'),
                    )

            if container.database_backup_enabled:
                instance = container.instance
                # ping = instance.ping()
                ping = 0
                self.logger.info(
                    ' - %s (is_ready=%s) -> %s',
                    instance.container_type,
                    ping == 0,
                    instance.backup_destination_path(),
                )
                if ping != 0:
                    self.logger.error("Database '%s' in service %s cannot be reached",
                                instance.container_type, container.service_name)

        if len(backup_containers) == 0:
            self.logger.info("No containers in the project has 'restic-compose-backup.*' label")

        self.logger.info("-" * 67)
