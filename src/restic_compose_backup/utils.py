import os
import logging
from typing import List, Tuple, TYPE_CHECKING
from subprocess import Popen, PIPE
from contextlib import contextmanager
import docker

if TYPE_CHECKING:
    from restic_compose_backup.containers import Container

logger = logging.getLogger(__name__)
TRUE_VALUES = ['1', 'true', 'True', True, 1]


def docker_client():
    """
    Create a docker client from the following environment variables::

        DOCKER_HOST=unix://tmp/docker.sock
        DOCKER_TLS_VERIFY=1
        DOCKER_CERT_PATH=''
    """
    # NOTE: Remove this fallback in 1.0
    if not os.environ.get('DOCKER_HOST'):
        os.environ['DOCKER_HOST'] = 'unix://tmp/docker.sock'

    return docker.from_env()


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


def get_swarm_nodes():
    client = docker_client()
    # NOTE: If not a swarm node docker.errors.APIError is raised
    #       503 Server Error: Service Unavailable
    #       ("This node is not a swarm manager. Use "docker swarm init" or
    #       "docker swarm join" to connect this node to swarm and try again.")
    try:
        return client.nodes.list()
    except docker.errors.APIError:
        return []


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


def is_true(value) -> True:
    """
    Evaluates the truthfulness of a bool value in container labels
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
    """Temp-set environment variables"""
    old_val = os.environ.get(name)
    os.environ[name] = value
    try:
        yield
    finally:
        if old_val is None:
            del os.environ[name]
        else:
            os.environ[name] = old_val


def test():
    return run(['ls', '/volumes'])


def ping_mysql(host, port, username) -> int:
    """Check if the mysql is up and can be reached"""
    return run([
        'mysqladmin',
        'ping',
        '--host',
        host,
        '--port',
        port,
        '--user',
        username,
    ])


def ping_mariadb(host, port, username) -> int:
    """Check if the mariadb is up and can be reached"""
    return run([
        'mysqladmin',
        'ping',
        '--host',
        host,
        '--port',
        port,
        '--user',
        username,
    ])


def ping_postgres(host, port, username, password) -> int:
    """Check if postgres can be reached"""
    return run([
        "pg_isready",
        f"--host={host}",
        f"--port={port}",
        f"--username={username}",
    ])


def run(cmd: List[str]) -> int:
    """Run a command with parameters"""
    logger.debug('cmd: %s', ' '.join(cmd))
    child = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutdata, stderrdata = child.communicate()

    if stdoutdata.strip():
        log_std('stdout', stdoutdata.decode(),
                logging.DEBUG if child.returncode == 0 else logging.ERROR)

    if stderrdata.strip():
        log_std('stderr', stderrdata.decode(), logging.ERROR)

    logger.debug("returncode %s", child.returncode)
    return child.returncode


def run_capture_std(cmd: List[str]) -> Tuple[str, str]:
    """Run a command with parameters and return stdout, stderr"""
    logger.debug('cmd: %s', ' '.join(cmd))
    child = Popen(cmd, stdout=PIPE, stderr=PIPE)
    return child.communicate()


def log_std(source: str, data: str, level: int):
    if isinstance(data, bytes):
        data = data.decode()

    if not data.strip():
        return

    log_func = logger.debug if level == logging.DEBUG else logger.error
    log_func('%s %s %s', '-' * 10, source, '-' * 10)

    lines = data.split('\n')
    if lines[-1] == '':
        lines.pop()

    for line in lines:
        log_func(line)

    log_func('-' * 28)
