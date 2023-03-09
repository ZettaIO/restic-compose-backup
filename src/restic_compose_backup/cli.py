import argparse
import logging
from typing import List

from restic_compose_backup import commands, log


def main():
    """Main entry point for the application"""
    args = parse_args(sorted(commands.COMMANDS.keys()))
    command = commands.COMMANDS[args.action](args)
    command.run()


def parse_args(choices: List[str]):
    parser = argparse.ArgumentParser(prog='restic_compose_backup')
    parser.add_argument(
        'action',
        choices=choices,
    )
    parser.add_argument(
        '--log-level',
        default=None,
        choices=list(log.LOG_LEVELS.keys()),
        help="Log level"
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
