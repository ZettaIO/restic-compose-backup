import os
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
        auto_remove=True,
        detach=True,
        environment=enviroment,
        volumes=volumes,
        working_dir=os.getcwd(),
    )

    print("Backup process container:", container.name)
    logs = container.logs(stdout=True, stderr=True, stream=True)
    try:
        while True:
            time.sleep(3)
            for line in logs:
                print(line.decode(), end='')
            # Raises requests.exceptions.HTTPError if continer is dead
            container.top()
    except Exception as ex:
        print("Container stopped")
