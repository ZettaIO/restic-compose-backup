import logging
from typing import List, Tuple
from subprocess import Popen, PIPE

logger = logging.getLogger(__name__)


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

    if stdoutdata:
        logger.debug(stdoutdata.decode().strip())
        logger.debug('-' * 28)

    if stderrdata:
        logger.error('%s STDERR %s', '-' * 10, '-' * 10)
        logger.error(stderrdata.decode().strip())
        logger.error('-' * 28)

    logger.debug("returncode %s", child.returncode)
    return child.returncode


def run_capture_std(cmd: List[str]) -> Tuple[str, str]:
    """Run a command with parameters and return stdout, stderr"""
    logger.debug('cmd: %s', ' '.join(cmd))
    child = Popen(cmd, stdout=PIPE, stderr=PIPE)
    return child.communicate()
