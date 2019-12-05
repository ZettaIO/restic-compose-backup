"""
Restic commands
"""
import logging
from typing import List, Tuple
from subprocess import Popen, PIPE
from restic_compose_backup import commands

logger = logging.getLogger(__name__)


def init_repo(repository: str):
    """
    Attempt to initialize the repository.
    Doing this after the repository is initialized
    """
    return commands.run(restic(repository, [
        "init",
    ]))


def backup_files(repository: str, source='/volumes'):
    return commands.run(restic(repository, [
        "--verbose",
        "backup",
        source,
    ]))


def backup_from_stdin(repository: str, filename: str, source_command: List[str]):
    """
    Backs up from stdin running the source_command passed in.
    It will appear in restic with the filename (including path) passed in.
    """
    dest_command = restic(repository, [
        'backup',
        '--stdin',
        '--stdin-filename',
        filename,
    ])

    # pipe source command into dest command
    # NOTE: Using the default buffer size: io.DEFAULT_BUFFER_SIZE = 8192
    #       We might want to tweak that to speed up large dumps.
    #       Actual tests tests must be done.
    source_process = Popen(source_command, stdout=PIPE)
    dest_process = Popen(dest_command, stdin=source_process.stdout, stdout=PIPE, stderr=PIPE)
    stdout, stderr = dest_process.communicate()

    if stdout:
        for line in stdout.decode().split('\n'):
            logger.debug(line)

    if stderr:
        for line in stderr.decode().split('\n'):
            logger.error(line)

    # Ensure both processes exited with code 0
    source_exit, dest_exit = source_process.poll(), dest_process.poll()
    return 0 if (source_exit == 0 and dest_exit == 0) else 1


def snapshots(repository: str, last=True) -> Tuple[str, str]:
    args = ["snapshots"]
    if last:
        args.append('--last')
    return commands.run_capture_std(restic(repository, args))


def forget(repository: str, daily: str, weekly: str, monthly: str, yearly: str):
    return commands.run(restic(repository, [
        'forget',
        '--keep-daily',
        daily,
        '--keep-weekly',
        weekly,
        '--keep-monthly',
        monthly,
        '--keep-yearly',
        yearly,
    ]))


def prune(repository: str):
    return commands.run(restic(repository, [
        'prune',
    ]))


def check(repository: str):
    return commands.run(restic(repository, [
        "check",
    ]))


def restic(repository: str, args: List[str]):
    """Generate restic command"""
    return [
        "restic",
        "-r",
        repository,
    ] + args
