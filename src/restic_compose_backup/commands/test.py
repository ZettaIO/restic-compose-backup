from .base import BaseCommand
from restic_compose_backup import utils

class Command(BaseCommand):
    """Test a command"""
    name = "test"

    def run(self):
        """Random test command"""
        nodes = utils.get_swarm_nodes()
        print("Swarm nodes:")
        for node in nodes:
            addr = node.attrs['Status']['Addr']
            state = node.attrs['Status']['State']
            print(' - {} {} {}'.format(node.id, addr, state))
