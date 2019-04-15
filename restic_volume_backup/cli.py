from restic_volume_backup.config import Config
from restic_volume_backup.containers import RunningContainers


def main():
    if len(sys.argv) < 2:
        raise ValueError("Missing argument: {}".format(cmds))

    mode = sys.argv[1]
    if mode not in cmds:
        raise ValueError("Valid arguments: {}".format(cmds))

    Config.check()

    containers = RunningContainers()

    if mode == 'status':
        containers.print_services()
        # volumes = containers.volume_mounts()
        # for vol in volumes:
        #     print(vol)
        #     print(vol.mount_string())

        # binds = containers.bind_mounts()
        # for vol in binds:
        #     print(binds)
        #     print(vol.mount_string())

    if mode == 'backup':
        print("Starting backup ..")
        # TODO: Errors when repo already exists
        # restic.init_repo(Config.repository)

        # for vol in containers.backup_volumes():
        #     restic.backup_volume(Config.repository, vol)

    if mode == 'snapshots':
        restic.snapshots(Config.repository)


if __name__ == '__main__':
    main()
