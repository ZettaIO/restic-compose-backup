"""
rcon-cli commands
"""
import logging
from typing import List, Tuple
from subprocess import Popen, PIPE
from restic_compose_backup import (
    commands,
    containers
)
from restic_compose_backup import utils

logger = logging.getLogger(__name__)

def rcon_cli(host, port, cmd: str) -> int:
    exit_code = commands.run([
        "rcon-cli",
        f"--host={host}",
        f"--port={port}",
        cmd
    ])

    if exit_code != 0:
        raise RconException(f"rcon-cli {cmd} exited with a non-zero exit code: {exit_code}")

    return exit_code

def is_online(host, port) -> int:
    """Check if rcon can be reached"""
    return rcon_cli(host, port, "help")

def save_off(host, port) -> int:
    """Turn saving off"""
    return rcon_cli(host, port, "save-off")

def save_on(host, port) -> int:
    """Turn saving on"""
    return rcon_cli(host, port, "save-on")

def save_all(host, port) -> int:
    """Save all worlds"""
    return rcon_cli(host, port, "save-all")


def sync(host, port) -> int:
    """sync data"""
    return rcon_cli(host, port, "sync")


class RconException(Exception):
    """Raised when an error occured while using the rcon-cli"""

    def __init__(self, message):
        self.message = message
