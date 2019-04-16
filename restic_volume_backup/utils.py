import docker

from restic_volume_backup.config import Config


def list_containers():
    """Easily mockable container list"""
    config = Config()
    client = docker.Client(base_url=config.docker_base_url)
    all_containers = client.containers()
    client.close()
    return all_containers
