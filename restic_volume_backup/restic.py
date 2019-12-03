"""
Restic commands
"""
import logging
from subprocess import Popen, PIPE
from restic_volume_backup import commands

logger = logging.getLogger(__name__)


def init_repo(repository):
    """
    Attempt to initialize the repository.
    Doing this after the repository is initialized
    """
    return commands.run([
        "restic",
        "--cache-dir",
        "/restic_cache",
        "-r",
        repository,
        "init",
    ])


def backup_files(repository, source='/backup'):
    return commands.run([
        "restic",
        "--cache-dir",
        "/restic_cache",
        "-r",
        repository,
        "--verbose",
        "backup",
        source,
    ])


def backup_mysql_all(repository, host, port, user, password, filename):
    """Backup all mysql databases"""
    # -h host, -p password
    return commands.run([
        'mysqldump',
        '--host',
        host,
        '--port',
        port,
        '--user',
        user,
        '--password',
        password,
        '|',
        'restic',
        'backup',
        '--stdin',
        '--stdin-filename',
        'dump.sql'
    ])


def backup_mysql_database(repository, host, port, user, password, filename, database):
    """Backup a single database"""
    pass


def snapshots(repository):
    return commands.run([
        "restic",
        "--cache-dir",
        "/restic_cache",
        "-r",
        repository,
        "snapshots",
    ])


def check(repository):
    return commands.run([
        "restic",
        "--cache-dir",
        "/restic_cache",
        "-r",
        repository,
        "check",
    ])
