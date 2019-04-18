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
        print()
        print("Backup config for compose project '{}'".format(containers.this_container.project_name))
        print()

        for container in containers.containers:
            print('service: {}'.format(container.service_name))
            for mount in container.filter_mounts():
                print(' - {}'.format(mount.source))

        print()

    elif args.action == 'backup':
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
            labels={"restic-volume-backup.backup_process": 'True'},
        )

    # Separate command to avoid spawning infinite containers :)
    elif args.action == 'start-backup-process':
        print("start-backup-process")
        import os
        print(os.environ)


def parse_args():
    parser = argparse.ArgumentParser(prog='restic_volume_backup')
    parser.add_argument(
        'action',
        choices=['status', 'backup', 'start-backup-process'],
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
