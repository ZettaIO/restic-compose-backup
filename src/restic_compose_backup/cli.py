import argparse
import os
import logging
from typing import List

from restic_compose_backup import (
    alerts,
    backup_runner,
    log,
    restic,
)
from restic_compose_backup.config import Config
from restic_compose_backup.containers import RunningContainers
from restic_compose_backup import utils
from restic_compose_backup import commands

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the application"""
    args = parse_args(sorted(commands.COMMANDS.keys()))
    command = commands.COMMANDS[args.action](args)
    command.run()
    return

    # Ensure log level is propagated to parent container if overridden
    # if args.log_level:
    #     containers.this_container.set_config_env('LOG_LEVEL', args.log_level)

    if args.action == 'status':
        status(config, containers)

    elif args.action == 'snapshots':
        snapshots(config, containers)

    elif args.action == 'backup':
        backup(config, containers)

    elif args.action == 'start-backup-process':
        start_backup_process(config, containers)

    elif args.action == 'cleanup':
        cleanup(config, containers)

    elif args.action == 'alert':
        alert(config, containers)

    # Random test stuff here
    elif args.action == "test":
        nodes = utils.get_swarm_nodes()
        print("Swarm nodes:")
        for node in nodes:
            addr = node.attrs['Status']['Addr']
            state = node.attrs['Status']['State']
            print(' - {} {} {}'.format(node.id, addr, state))


def backup(config, containers):
    """Request a backup to start"""
    # Make sure we don't spawn multiple backup processes
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

    logger.debug('Starting backup container with image %s', containers.this_container.image)
    try:
        result = backup_runner.run(
            image=containers.this_container.image,
            command='restic-compose-backup start-backup-process',
            volumes=volumes,
            environment=containers.this_container.environment,
            source_container_id=containers.this_container.id,
            labels={
                containers.backup_process_label: 'True',
                "com.docker.compose.project": containers.project_name,
            },
        )
    except Exception as ex:
        logger.exception(ex)
        alerts.send(
            subject="Exception during backup",
            body=str(ex),
            alert_type='ERROR',
        )
        return

    logger.info('Backup container exit code: %s', result)

    # Alert the user if something went wrong
    if result != 0:
        alerts.send(
            subject="Backup process exited with non-zero code",
            body=open('backup.log').read(),
            alert_type='ERROR',
        )


def start_backup_process(config, containers):
    """The actual backup process running inside the spawned container"""
    if not utils.is_true(os.environ.get('BACKUP_PROCESS_CONTAINER')):
        logger.error(
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

    status(config, containers)
    errors = False

    # Did we actually get any volumes mounted?
    try:
        has_volumes = os.stat('/volumes') is not None
    except FileNotFoundError:
        logger.warning("Found no volumes to back up")
        has_volumes = False

    # Warn if there is nothing to do
    if len(containers.containers_for_backup()) == 0 and not has_volumes:
        logger.error("No containers for backup found")
        exit(1)

    if has_volumes:
        try:
            logger.info('Backing up volumes')
            vol_result = restic.backup_files(config.repository, source='/volumes')
            logger.debug('Volume backup exit code: %s', vol_result)
            if vol_result != 0:
                logger.error('Volume backup exited with non-zero code: %s', vol_result)
                errors = True
        except Exception as ex:
            logger.error('Exception raised during volume backup')
            logger.exception(ex)
            errors = True

    # back up databases
    logger.info('Backing up databases')
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
                logger.exception(ex)
                errors = True

    if errors:
        logger.error('Exit code: %s', errors)
        exit(1)

    # Only run cleanup if backup was successful
    result = cleanup(config, container)
    logger.debug('cleanup exit code: %s', result)
    if result != 0:
        logger.error('cleanup exit code: %s', result)
        exit(1)

    # Test the repository for errors
    logger.info("Checking the repository for errors")
    result = restic.check(config.repository)
    if result != 0:
        logger.error('Check exit code: %s', result)
        exit(1)

    logger.info('Backup completed')


def cleanup(config, containers):
    """Run forget / prune to minimize storage space"""
    logger.info('Forget outdated snapshots')
    forget_result = restic.forget(
        config.repository,
        config.keep_daily,
        config.keep_weekly,
        config.keep_monthly,
        config.keep_yearly,
    )
    logger.info('Prune stale data freeing storage space')
    prune_result = restic.prune(config.repository)
    return forget_result and prune_result


def snapshots(config, containers):
    """Display restic snapshots"""
    stdout, stderr = restic.snapshots(config.repository, last=True)
    for line in stdout.decode().split('\n'):
        print(line)


def parse_args(choices: List[str]):
    parser = argparse.ArgumentParser(prog='restic_compose_backup')
    parser.add_argument(
        'action',
        choices=choices,
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
