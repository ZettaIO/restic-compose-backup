"""
Restic commands
"""
import logging
from typing import List
from subprocess import Popen, PIPE
from restic_volume_backup import commands

logger = logging.getLogger(__name__)


def init_repo(repository: str):
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


def backup_files(repository: str, source='/backup'):
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


def backup_from_stdin(filename: str, source_command: List[str]):
    """
    Backs up from stdin running the source_command passed in.
    It will appear in restic with the filename (including path) passed in.
    """
    dest_command = [
        'restic',
        "--cache-dir",
        'backup',
        '--stdin',
        '--stdin-filename',
        filename,
    ]

    # pipe source command into dest command
    source_process = Popen(source_command, stdout=PIPE)
    dest_process = Popen(dest_command, stdin=source_process.stdout)
    return dest_process.communicate()


def snapshots(repository: str):
    return commands.run([
        "restic",
        "--cache-dir",
        "/restic_cache",
        "-r",
        repository,
        "snapshots",
    ])


def check(repository: str):
    return commands.run([
        "restic",
        "--cache-dir",
        "/restic_cache",
        "-r",
        repository,
        "check",
    ])
