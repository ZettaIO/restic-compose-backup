import os
import sys
import time
import docker

from restic_volume_backup.config import Config


def run(image: str = None, command: str = None, volumes: dict = None,
    enviroment: dict = None, labels: dict = None):
    config = Config()
    client = docker.DockerClient(base_url=config.docker_base_url)

    container = client.containers.run(
        image,
        command,
        labels=labels,
        # auto_remove=True,
        detach=True,
        environment=enviroment,
        volumes=volumes,
        working_dir=os.getcwd(),
        tty=True,
    )

    print("Backup process container:", container.name)
    log_generator = container.logs(stdout=True, stderr=True, stream=True, follow=True)
    with open('backup.log', 'w') as fd:
        for line in log_generator:
            line = line.decode()
            fd.write(line)
            print(line, end='')

    container.reload()
    print("ExitCode", container.attrs['State']['ExitCode'])
    container.remove()
