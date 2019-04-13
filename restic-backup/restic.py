import os
from subprocess import Popen, PIPE, check_call


def repo_path(container_name):
    return "swift:{}:/".format(container_name)


def init_repo(container_name):
    run_command([
        "restic",
        "-r",
        repo_path(container_name),
        "init",
    ])


def backup_volume(container_name, volume):
    run_command([
        "restic",
        "-r",
        repo_path(container_name),
        "--verbose",
        "backup",
        volume.destination,
    ])


def snapshots(container_name):
    run_command([
        "restic",
        "-r",
        repo_path(container_name),
        "snapshots",
    ])


def check(container_name):
    run_command([
        "restic",
        "-r",
        repo_path(container_name),
        "check",
    ])


def run_command(cmd):
    child = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutdata, stderrdata = child.communicate()

    if stdoutdata:
        print(stdoutdata.decode())

    if stderrdata:
        print(stderrdata.decode())
