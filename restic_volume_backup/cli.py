import argparse
import sys

from restic_volume_backup.config import Config
from restic_volume_backup.containers import RunningContainers
from restic_volume_backup import backup_runner
from restic_volume_backup import restic


def main():
    args = parse_args()
    config = Config()
    containers = RunningContainers()

    if args.action == 'status':
        status(config, containers)

    elif args.action == 'backup':
        backup(config, containers)

    # Separate command to avoid spawning infinite containers :)
    elif args.action == 'start-backup-process':
        start_backup_process(config, containers)


def status(config, containers):
    """Outputs the backup config for the compse setup"""
    print()
    print("Backup config for compose project '{}'".format(containers.this_container.project_name))
    print("Current service:", containers.this_container.name)
    print("Backup process :", containers.backup_process_container.name \
        if containers.backup_process_container else 'Not Running')
    print("Backup running :", containers.backup_process_running)

    print()

    for container in containers.containers:
        print('service: {}'.format(container.service_name))
        for mount in container.filter_mounts():
            print(' - {}'.format(mount.source))

    print()


def backup(config, containers):
    """Start backup"""
    # Make sure we don't spawn multiple backup processes
    if containers.backup_process_running:
        raise ValueError("Backup process already running")        

    print("Initializing repository")

    # TODO: Errors when repo already exists
    restic.init_repo(config.repository)

    print("Starting backup container..")
    backup_runner.run(
        image=containers.this_container.image,
        command='restic-volume-backup start-backup-process',
        volumes=containers.this_container.volumes,
        enviroment=containers.this_container.environment,
        labels={
            "restic-volume-backup.backup_process": 'True',
            "com.docker.compose.project": containers.this_container.project_name,
        },
    )


def start_backup_process(config, containers):
    """Start the backup process container"""
    if not containers.backup_process_container or containers.this_container == containers.backup_process_container is False:
        print(
            "Cannot run backup process in this container. Use backup command instead. "
            "This will spawn a new container with the necessary mounts."
        )
        return

    print("start-backup-process")
    status(config, containers)
    import time
    for i in range(5):
        time.sleep(1)
        print(i)

    exit(1)

def parse_args():
    parser = argparse.ArgumentParser(prog='restic_volume_backup')
    parser.add_argument(
        'action',
        choices=['status', 'backup', 'start-backup-process'],
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
