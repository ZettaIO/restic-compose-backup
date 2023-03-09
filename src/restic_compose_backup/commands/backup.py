from .base import BaseCommand
from restic_compose_backup import backup_runner, alerts


class Command(BaseCommand):
    """Backup a directory"""
    name = "backup"

    def run(self):
        """Run the backup command"""
        containers = self.get_containers()

        if containers.backup_process_running:
            alerts.send(
                subject="Backup process container already running",
                body=(
                    "A backup process container is already running. \n"
                    f"Id: {containers.backup_process_container.id}\n"
                    f"Name: {containers.backup_process_container.name}\n"
                ),
                alert_type='ERROR',
            )
            raise RuntimeError("Backup process already running")

        # Map all volumes from the backup container into the backup process container
        volumes = containers.this_container.volumes

        # Map volumes from other containers we are backing up
        mounts = containers.generate_backup_mounts('/volumes')
        volumes.update(mounts)

        self.logger.debug('Starting backup container with image %s', containers.this_container.image)
        try:
            result = backup_runner.run(
                image=containers.this_container.image,
                command='restic-compose-backup start_backup_process',
                volumes=volumes,
                environment=containers.this_container.environment,
                source_container_id=containers.this_container.id,
                labels={
                    containers.backup_process_label: 'True',
                    "com.docker.compose.project": containers.project_name,
                },
            )
        except Exception as ex:
            self.logger.exception(ex)
            alerts.send(
                subject="Exception during backup",
                body=str(ex),
                alert_type='ERROR',
            )
            return

        self.logger.info('Backup container exit code: %s', result)

        # Alert the user if something went wrong
        if result != 0:
            alerts.send(
                subject="Backup process exited with non-zero code",
                body=open('backup.log').read(),
                alert_type='ERROR',
            )
