import docker

from restic_volume_backup.config import Config


def list_containers():
    """
    List all containers.

    Returns:
        List of raw container json data from the api
    """
    config = Config()
    client = docker.DockerClient(base_url=config.docker_base_url)
    all_containers = client.containers.list()
    client.close()
    return [c.attrs for c in all_containers]
