import unittest
from unittest import mock

from restic_volume_backup import utils


def list_containers():
    return {}


@mock.patch('restic_volume_backup.utils.list_containers', list_containers)
class ResticBackupTests(unittest.TestCase):

    def test_stuff(self):
        assert utils.list_containers() == {}
