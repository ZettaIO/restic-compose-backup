import os
import sys
from containers import RunningContainers
import restic

cmds = ['volumes', 'backup', 'snapshots', 'check']


class Config:
    container_name = os.environ['CONTAINER_NAME']
    password = os.environ['RESTIC_PASSWORD']

    @classmethod
    def check(cls):
        if not cls.container_name:
            raise ValueError("CONTAINER env var not set")

        if not cls.password:
            raise ValueError("PASSWORD env var not set")


def main():
    if len(sys.argv) < 2:
        raise ValueError("Missing argument: {}".format(cmds))

    mode = sys.argv[1]
    if mode not in cmds:
        raise ValueError("Valid arguments: {}".format(cmds))

    Config.check()

    containers = RunningContainers()

    if mode == 'volumes':
        volumes = containers.volume_mounts()
        for vol in volumes:
            print(vol)
            print(vol.mount_string())

        binds = containers.bind_mounts()
        for vol in binds:
            print(vol.mount_string())

    if mode == 'backup':
        restic.init_repo(Config.container_name)

        for vol in containers.backup_volumes():
            restic.backup_volume(Config.container_name, vol)

    if mode == 'snapshots':
        restic.snapshots(Config.container_name)

if __name__ == '__main__':
    main()
