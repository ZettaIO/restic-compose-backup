import os
from contextlib import contextmanager
import docker

from restic_compose_backup.config import Config

TRUE_VALUES = ['1', 'true', 'True', True, 1]


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


def is_true(value):
    """
    Evaluates the truthfullness of a bool value in container labels
    """
    return value in TRUE_VALUES


def strip_root(path):
    """
    Removes the root slash in a path.
    Example: /srv/data becomes srv/data
    """
    path = path.strip()
    if path.startswith('/'):
        return path[1:]

    return path


@contextmanager
def environment(name, value):
    """Tempset env var"""
    old_val = os.environ.get(name)
    os.environ[name] = value
    try:
        yield
    finally:
        if old_val is None:
            del os.environ[name]
        else:
            os.environ[name] = old_val
