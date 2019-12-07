import os
import logging
from typing import List
from contextlib import contextmanager
import docker
from restic_compose_backup.config import Config

logger = logging.getLogger(__name__)

TRUE_VALUES = ['1', 'true', 'True', True, 1]


def docker_client():
    config = Config()
    return docker.DockerClient(base_url=config.docker_base_url)


def list_containers() -> List[dict]:
    """
    List all containers.

    Returns:
        List of raw container json data from the api
    """
    client = docker_client()
    all_containers = client.containers.list(all=True)
    client.close()
    return [c.attrs for c in all_containers]


def remove_containers(containers: List['Container']):
    client = docker_client()
    logger.info('Attempting to delete stale backup process containers')
    for container in containers:
        logger.info(' -> deleting %s', container.name)
        try:
            c = client.containers.get(container.name)
            c.remove()
        except Exception as ex:
            logger.exception(ex)


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
