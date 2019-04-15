import argparse
import sys

from restic_volume_backup.config import Config
from restic_volume_backup.containers import RunningContainers


def main():
    args = parse_args()

    Config.check()

    containers = RunningContainers()

    if args.action == 'status':
        containers.print_services()
        # volumes = containers.volume_mounts()
        # for vol in volumes:
        #     print(vol)
        #     print(vol.mount_string())

        # binds = containers.bind_mounts()
        # for vol in binds:
        #     print(binds)
        #     print(vol.mount_string())

    elif args.mode == 'backup':
        print("Starting backup ..")
        # TODO: Errors when repo already exists
        # restic.init_repo(Config.repository)

        # for vol in containers.backup_volumes():
        #     restic.backup_volume(Config.repository, vol)

    elif args.mode == 'snapshots':
        restic.snapshots(Config.repository)


def parse_args():
    parser = argparse.ArgumentParser(prog='restic_volume_backup')
    parser.add_argument(
        'action',
        choices=['status', 'backup'],
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
