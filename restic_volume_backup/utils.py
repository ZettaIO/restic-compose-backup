import docker

from restic_volume_backup.config import Config


def list_containers():
    """Easily mockable container list"""
    client = docker.Client(base_url=Config.docker_base_url)
    all_containers = client.containers()
    client.close()
    return all_containers
