import os
import docker

from restic_volume_backup.config import Config

def run():
    config = Config()
    client = docker.DockerClient(base_url=config.docker_base_url)

    container = client.containers.run(
        'restic-volume-backup_backup',
        'echo "Hello"',
        labels={"restic-volume-backup.backup_process": 'True'},
        auto_remove=True,
        remove=True,
        detach=True,
        environment={
            'test1': 'value1',
            'test2': 'value2',
        },
        volumes={
            '/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
            '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'},
        },
        working_dir=os.getcwd(),
    )

    # Pull logs and exist status of container
