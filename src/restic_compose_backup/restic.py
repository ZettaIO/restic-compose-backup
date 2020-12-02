"""
Restic commands
"""
import logging
import os.path
from typing import List, Tuple
from subprocess import Popen, PIPE
from restic_compose_backup import commands, utils

logger = logging.getLogger(__name__)


def init_repo(repository: str):
    """
    Attempt to initialize the repository.
    Doing this after the repository is initialized
    """
    return commands.run(restic(repository, [
        "init",
    ]))


def backup_files(repository: str, source='/volumes', tags=''):
    args = [
        "--verbose",
        "backup",
        source
    ]

    excludes_file = os.path.join(source, "excludes.txt")
    if os.path.isfile(excludes_file):
        args.extend(['--exclude-file', excludes_file])

    args.extend(utils.format_tags(tags))
    return commands.run(restic(repository, args))


def backup_from_stdin(repository: str, filename: str, source_command: List[str], tags=''):
    """
    Backs up from stdin running the source_command passed in.
    It will appear in restic with the filename (including path) passed in.
    """
    args = [
        'backup',
        '--stdin',
        '--stdin-filename',
        filename,
    ]
    args.extend(utils.format_tags(tags))
    dest_command = restic(repository, args)

    # pipe source command into dest command
    source_process = Popen(source_command, stdout=PIPE, bufsize=65536)
    dest_process = Popen(dest_command, stdin=source_process.stdout, stdout=PIPE, stderr=PIPE, bufsize=65536)
    stdout, stderr = dest_process.communicate()

    # Ensure both processes exited with code 0
    source_exit, dest_exit = source_process.poll(), dest_process.poll()
    exit_code = 0 if (source_exit == 0 and dest_exit == 0) else 1

    if stdout:
        commands.log_std('stdout', stdout, logging.DEBUG if exit_code == 0 else logging.ERROR)

    if stderr:
        commands.log_std('stderr', stderr, logging.ERROR)

    return exit_code


def snapshots(repository: str, last=True) -> Tuple[str, str]:
    """Returns the stdout and stderr info"""
    args = ["snapshots"]
    if last:
        args.append('--last')
    return commands.run_capture_std(restic(repository, args))


def is_initialized(repository: str) -> bool:
    """
    Checks if a repository is initialized using snapshots command.
    Note that this cannot separate between uninitalized repo
    and other errors, but this method is reccomended by the restic
    community.
    """
    return commands.run(restic(repository, ["snapshots", '--last'])) == 0


def forget(repository: str, keeplast: str, hourly: str, daily: str, weekly: str, monthly: str, yearly: str, keep_tags='', filter_tags=''):
    args = [
        'forget',
        '--group-by',
        'paths,tags',
        '--keep-last',
        keeplast,
        '--keep-hourly',
        hourly,
        '--keep-daily',
        daily,
        '--keep-weekly',
        weekly,
        '--keep-monthly',
        monthly,
        '--keep-yearly',
        yearly
    ]
    args.extend(utils.format_tags(keep_tags, '--keep-tag'))
    args.extend(utils.format_tags(filter_tags))
    return commands.run(restic(repository, args))


def prune(repository: str):
    return commands.run(restic(repository, [
        'prune',
    ]))


def check(repository: str):
    return commands.run(restic(repository, [
        "check",
        # "--with-cache",
    ]))


def restic(repository: str, args: List[str]):
    """Generate restic command"""
    return [
        "restic",
        "-r",
        repository,
    ] + args
