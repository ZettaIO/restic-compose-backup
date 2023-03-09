import logging
from restic_compose_backup.config import Config
from restic_compose_backup.containers import RunningContainers
from restic_compose_backup import log


class BaseCommand:
    """Base class for all commands"""
    name = "base"

    def __init__(self, cli_args, *args, **kwargs):
        self.cli_args = cli_args
        self.log_level = cli_args.log_level
        self.config = Config()
        log.setup(level=self.log_level or self.config.log_level)
        self.logger = log.logger

    def get_containers(self):
        """Get running containers"""
        containers = RunningContainers()
        containers.this_container.set_config_env('LOG_LEVEL', self.log_level)
        return containers

    def run(self):
        """Run the command"""
        raise NotImplementedError

    def run_command(self, command: str):
        """Run a command by name and return the result"""
        from . import COMMANDS
        command = COMMANDS[command]
        command(self.cli_args).run()
