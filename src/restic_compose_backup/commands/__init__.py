import sys
from importlib import import_module
from pkgutil import iter_modules
from typing import Dict
from .base import BaseCommand


def get_commands() -> Dict[str, BaseCommand]:
    """Return the list of available command classes"""
    _commands = {}
    current_module = sys.modules[__name__]
    for module_info in iter_modules(current_module.__path__):
        module = import_module(f'restic_compose_backup.commands.{module_info.name}')
        if hasattr(module, 'Command'):
            _commands[module_info.name] = module.Command
    return _commands


COMMANDS = get_commands()
