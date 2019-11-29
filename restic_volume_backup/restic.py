import logging
from subprocess import Popen, PIPE

logger = logging.getLogger(__name__)

def test():
    return run_command(['ls', '/backup'])


def init_repo(repository):
    """
    Attempt to initialize the repository.
    Doing this after the repository is initialized
    """
    return run_command([
        "restic",
        "--cache-dir",
        "/restic_cache",
        "-r",
        repository,
        "init",
    ])


def backup_files(repository, source='/backup'):
    return run_command([
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
    return run_command([
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


def ping_mysql(host, port, username, password):
    """Check if the database is up and can be reached"""
    return run_command([
        'mysqladmin',
        'ping',
        '--host',
        host,
        '--port',
        port,
        '--user',
        username,
        f'--password={password}',
    ])

def snapshots(repository):
    return run_command([
        "restic",
        "--cache-dir",
        "/restic_cache",
        "-r",
        repository,
        "snapshots",
    ])


def check(repository):
    return run_command([
        "restic",
        "--cache-dir",
        "/restic_cache",
        "-r",
        repository,
        "check",
    ])


def run_command(cmd):
    logger.info('cmd: %s', ' '.join(cmd))
    child = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutdata, stderrdata = child.communicate()

    if stdoutdata:
        logger.info(stdoutdata.decode().strip())
        logger.info('-' * 28)

    if stderrdata:
        logger.info('%s STDERR %s', '-' * 10, '-' * 10)
        logger.info(stderrdata.decode().strip())
        logger.info('-' * 28)

    logger.info("returncode %s", child.returncode)
    return child.returncode
