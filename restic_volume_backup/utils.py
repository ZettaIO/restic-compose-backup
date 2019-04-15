import docker
import pprint

from restic_volume_backup.config import Config


def list_containers():
    client = docker.Client(base_url=Config.docker_base_url)
    all_containers = client.containers()
    pprint.pprint(all_containers, indent=2)
    client.close()
    return all_containers
