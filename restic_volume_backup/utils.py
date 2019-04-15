import docker


def list_containers():
    client = docker.Client(base_url=DOCKER_BASE_URL)
    all_containers = client.containers()
    client.close()
    return all_containers
