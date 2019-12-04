import argparse
import pprint
import logging

from restic_compose_backup import (
    alerts,
    backup_runner,
    log,
    restic,
)
from restic_compose_backup.config import Config
from restic_compose_backup.containers import RunningContainers

logger = logging.getLogger(__name__)


def main():
    """CLI entrypoint"""
    args = parse_args()
    log.setup(level=args.log_level)
    config = Config()
    containers = RunningContainers()

    if args.action == 'status':
        status(config, containers)

    elif args.action == 'snapshots':
        snapshots(config, containers)

    elif args.action == 'backup':
        backup(config, containers)

    elif args.action == 'start-backup-process':
        start_backup_process(config, containers)

    elif args.action == 'alert':
        alert(config, containers)


def status(config, containers):
    """Outputs the backup config for the compose setup"""
    logger.info("Status for compose project '%s'", containers.project_name)
    logger.info("Backup currently running?: %s", containers.backup_process_running)
    logger.info("%s Detected Config %s", "-" * 25, "-" * 25)

    backup_containers = containers.containers_for_backup()
    for container in backup_containers:
        logger.info('service: %s', container.service_name)

        if container.volume_backup_enabled:
            for mount in container.filter_mounts():
                logger.info(' - volume: %s', mount.source)

        if container.database_backup_enabled:
            instance = container.instance
            ping = instance.ping()
            logger.info(' - %s (is_ready=%s)', instance.container_type, ping == 0)
            if ping != 0:
                logger.error("Database '%s' in service %s cannot be reached", instance.container_type, container.service_name)

    if len(backup_containers) == 0:
        logger.info("No containers in the project has 'restic-compose-backup.enabled' label")

    logger.info("-" * 67)

def snapshots(config, containers):
    """Display restic snapshots"""
    stdout, stderr = restic.snapshots(config.repository)
    for line in stdout.decode().split('\n'):
        logger.info('| %s', line)


def backup(config, containers):
    """Request a backup to start"""
    # Make sure we don't spawn multiple backup processes
    if containers.backup_process_running:
        raise ValueError("Backup process already running")

    logger.info("Initializing repository (may fail if already initalized)")

    # TODO: Errors when repo already exists
    restic.init_repo(config.repository)

    # Map all volumes from the backup container into the backup process container
    volumes = containers.this_container.volumes

    # Map volumes from other containers we are backing up
    mounts = containers.generate_backup_mounts('/backup')
    volumes.update(mounts)

    result = backup_runner.run(
        image=containers.this_container.image,
        command='restic-compose-backup start-backup-process',
        volumes=volumes,
        environment=containers.this_container.environment,
        source_container_id=containers.this_container.id,
        labels={
            "restic-compose-backup.backup_process": 'True',
            "com.docker.compose.project": containers.project_name,
        },
    )
    logger.info('Backup container exit code: %s', result)


def start_backup_process(config, containers):
    """The actual backup process running inside the spawned container"""
    if (not containers.backup_process_container
       or containers.this_container == containers.backup_process_container is False):
        logger.error(
            "Cannot run backup process in this container. Use backup command instead. "
            "This will spawn a new container with the necessary mounts."
        )
        return

    status(config, containers)
    errors = False

    # Back up volumes
    try:
        logger.info('Backing up volumes')
        vol_result = restic.backup_files(config.repository, source='/backup')
        logger.debug('Volume backup exit code: %s', vol_result)
        if vol_result != 0:
            logger.error('Backup command exited with non-zero code: %s', vol_result)
            errors = True
    except Exception as ex:
        logger.error(ex)
        errors = True

    # back up databases
    for container in containers.containers_for_backup():
        if container.database_backup_enabled:
            try:
                instance = container.instance
                logger.info('Backing up %s in service %s', instance.container_type, instance.service_name)
                result = instance.backup()
                logger.debug('Exit code: %s', result)
                if result != 0:
                    logger.error('Backup command exited with non-zero code: %s', result)
                    errors = True
            except Exception as ex:
                logger.error(ex)
                errors = True

    # Alert the user if something went wrong
    if errors:
        alerts.send(
            subject="Backup process exited with non-zero code",
            body=open('backup.log').read(),
            alert_type='ERROR',
        )


def alert(config, containers):
    """Test alerts"""
    logger.info("Testing alerts")
    alerts.send(
        subject="{}: Test Alert".format(containers.project_name),
        body="Test message",
    )


def parse_args():
    parser = argparse.ArgumentParser(prog='restic_compose_backup')
    parser.add_argument(
        'action',
        choices=['status', 'snapshots', 'backup', 'start-backup-process', 'alert'],
    )
    parser.add_argument(
        '--log-level',
        default=None,
        choices=list(log.LOG_LEVELS.keys()),
        help="Log level"
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
