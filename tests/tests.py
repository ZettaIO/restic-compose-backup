import json
import os
import unittest
from unittest import mock

from restic_volume_backup import utils
import fixtures

list_containers_func = 'restic_volume_backup.utils.list_containers'

class ResticBackupTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up basic enviroment variables"""
        os.environ['RESTIC_REPOSITORY'] = "test"
        os.environ['RESTIC_PASSWORD'] = "password"

    def test_stuff(self):
        containers = [
            {
                'service': 'web',
                'labels': {
                    'moo': 1,
                },
                'mounts': [{
                    'Source': 'moo',
                    'Destination': 'moo',
                    'Type': 'bind',
                }]
            },
            {
                'service': 'mysql',
            },
            {
                'service': 'postgres',
            },
        ]

        with mock.patch(list_containers_func, fixtures.containers(containers=containers)):
            test = utils.list_containers()

        # raise ValueError(json.dumps(test, indent=2))
