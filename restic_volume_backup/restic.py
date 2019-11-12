from subprocess import Popen, PIPE


def init_repo(repository):
    run_command([
        "restic",
        "-r",
        repository,
        "init",
    ])


def backup_volume(repository, volume):
    run_command([
        "restic",
        "-r",
        repository,
        "--verbose",
        "backup",
        volume.destination,
    ])


def snapshots(repository):
    run_command([
        "restic",
        "-r",
        repository,
        "snapshots",
    ])


def check(repository):
    run_command([
        "restic",
        "-r",
        repository,
        "check",
    ])


def run_command(cmd):
    child = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutdata, stderrdata = child.communicate()

    if stdoutdata:
        print(stdoutdata.decode())

    if stderrdata:
        print(stderrdata.decode())
