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
        if containers.backup_process_running:
            raise ValueError("Backup process alredy running")

        print("Initializing repository")

        # TODO: Errors when repo already exists
        restic.init_repo(config.repository)

        print("Starting backup container..")
        backup_runner.run(
            containers.this_container.image,
            # "sleep 10",
            './test.sh',
        )
        # for vol in containers.backup_volumes():
        #     restic.backup_volume(Config.repository, vol)


def parse_args():
    parser = argparse.ArgumentParser(prog='restic_volume_backup')
    parser.add_argument(
        'action',
        choices=['status', 'backup'],
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
