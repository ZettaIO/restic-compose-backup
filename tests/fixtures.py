"""Generate test fixtures"""
from datetime import datetime
import hashlib
import string
import random


def generate_sha256():
    """Generate a unique sha256"""
    h = hashlib.sha256()
    h.update(str(datetime.now().timestamp()).encode())
    return h.hexdigest()


def containers(project="default", containers=[]):
    """
    Args:
        project (str): Name of the compose project
        containers (dict):
            {
                'containers: [
                    'id': 'something'
                    'service': 'service_name',
                    'mounts: [{
                        'Source': '/home/user/stuff',
                        'Destination': '/srv/stuff',
                        'Type': 'bind' / 'volume'
                    }],
                ]
            }
    """
    def wrapper(*args, **kwargs):
        return [
        {
            'Id': container.get('id', generate_sha256()),
            'Name': ''.join(random.choice(string.ascii_lowercase) for i in range(16)),
            'ImageID': 'sha256:4d9a81206af7d65563b85d06be160dc90dc20ade94edcf544261f0e1db4472b3',
            'Config': {
                'Image': 'restic-volume-backup_backup',
                'Labels': {
                    'com.docker.compose.oneoff': 'False',
                    'com.docker.compose.project': project,
                    'com.docker.compose.service': container['service'],
                    **container.get('labels', {}),
                },
            },
            'Mounts': container.get('mounts', []),
            'NetworkSettings': {
                'Networks': {
                    'restic-volume-backup_default': {
                        'Aliases': None,
                        'DriverOpts': None,
                        'EndpointID': '96ac233ec96ae2318a15419c4d211bbc0d130fc33baaaba6dcd8c13328ba4b8f',
                        'Gateway': '172.22.0.1',
                        'GlobalIPv6Address': '',
                        'GlobalIPv6PrefixLen': 0,
                        'IPAMConfig': None,
                        'IPAddress': '172.22.0.2',
                        'IPPrefixLen': 16,
                        'IPv6Gateway': '',
                        'Links': None,
                        'MacAddress': '02:42:ac:16:00:02',
                        'NetworkID': '98886e14fddc2b3d31d15fbbfc3ea1b339626374ba2ff6c2dad406b1617ee09c',
                    }
                }
            },
            'State': {
                "Status": "running",
                "Running": True,
            }
        }
        for container in containers]

    return wrapper
