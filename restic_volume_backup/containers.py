import os
import docker
import json
import pprint

from restic_volume_backup import utils

VOLUME_TYPE_BIND = "bind"
VOLUME_TYPE_VOLUME = "volume"


class Container:
    """Represents a docker container"""

    def __init__(self, data):
        self._data = data
        self.id = data['Id']
        self.name = data['Name']

        self._state = data.get('State')
        self._config = data.get('Config')
        self._mounts = [Mount(mnt, container=self) for mnt in data.get('Mounts')]

        if not self._state:
            raise ValueError('Container meta missing State')
        if self._config is None:
            raise ValueError('Container meta missing Config')

        self._labels = self._config.get('Labels')
        if self._labels is None:
            raise ValueError('Container mtea missing Config->Labels')

        self._include = self._parse_pattern(self.get_label('restic-volume-backup.include'))
        self._exclude = self._parse_pattern(self.get_label('restic-volume-backup.exclude'))

    @property
    def image(self):
        """Image name"""
        return self.get_config('Image')

    @property
    def environment(self):
        """All configured env vars for the container"""
        return self.get_config('Env', default=[])

    @property
    def volumes(self):
        """
        Return volumes for the container in the following format:
            {'/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},}
        """
        # {'Type': 'bind', 
        #  'Source': '/Users/einarforselv/Documents/projects/contraz/restic-volume-backup',
        #  'Destination': '/restic-volume-backup',
        #  'Mode': 'rw',
        #  'RW': True,
        #  'Propagation': 'rprivate'}
        volumes = {}
        for mount in self._mounts:
            volumes[mount.source] = {'bind': mount.destination, 'mode': 'ro'}

        return volumes

    @property
    def backup_enabled(self) -> bool:
        """Is backup enabled for this container?"""
        return self.get_label('restic-volume-backup.enabled') == 'True'

    @property
    def is_backup_process_container(self) -> bool:
        """Is this container the running backup process?"""
        return self.get_label('restic-volume-backup.backup_process') == 'True'

    @property
    def is_running(self) -> bool:
        """Is the container running?"""
        return self._state.get('Running', False)

    @property
    def service_name(self) ->str:
        """Name of the container/service"""
        return self.get_label('com.docker.compose.service', default='')

    @property
    def project_name(self) -> str:
        """Name of the compose setup"""
        return self.get_label('com.docker.compose.project', default='')

    @property
    def is_oneoff(self) -> bool:
        """Was this container started with run command?"""
        return self.get_label('com.docker.compose.oneoff', default='False') == 'True'

    def get_config(self, name, default=None):
        """Get value from config dict"""
        return self._config.get(name, default)

    def get_label(self, name, default=None):
        """Get a label by name"""
        return self._labels.get(name, None)

    def filter_mounts(self):
        """Get all mounts for this container matching include/exclude filters"""
        filtered = []
        if self._include:
            for mount in self._mounts:
                for pattern in self._include:
                    if pattern in mount.source:
                        break
                else:
                    continue

                filtered.append(mount)

        elif self._exclude:
            for mount in self._mounts:
                for pattern in self._exclude:
                    if pattern in mount.source:
                        break
                else:
                    filtered.append(mount)
        else:
            return self._mounts

        return filtered

    def _parse_pattern(self, value):
        if not value:
            return None

        if type(value) is not str:
            return None

        value = value.strip()
        if len(value) == 0:
            return None

        return value.split(',')

    def to_dict(self):
        return {
            'Id': self.id,
            'Names': self.names,
            'State': self.state,
            'Labels': self.labels,
            'Mounts': [mnt.data for mnt in self.mounts],
            'include': self.include,
            'exclude': self.exlude,
        }


class Mount:
    """Represents a volume mount (volume or bind)"""
    def __init__(self, data, container=None):
        self._data = data
        self._container = container

    @property
    def container(self) -> Container:
        """The container this mount belongs to"""
        return self._container

    @property
    def type(self) -> str:
        """bind/volume"""
        return self._data.get('Type')

    @property
    def name(self) -> str:
        """Name of the mount"""        
        return self._data.get('Name')

    @property
    def source(self) -> str:
        """Source of the mount. Volume name or path"""
        return self._data.get('Source')

    @property
    def destination(self) -> str:
        """Destionatin path for the volume mount in the container"""
        return self._data.get('Destination')

    def mount_string(self) -> str:
        if self.type == VOLUME_TYPE_VOLUME:
            return "- {}:{}:ro".format(self.name.split('_')[-1], self.destination)
        elif self.type == VOLUME_TYPE_BIND:
            return "- {}:{}:ro".format(self.source, self.destination)
        else:
            raise ValueError("Uknown volume type: {}".format(self.type))

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self._data)

    def __hash__(self):
        """Uniquness for a volume"""
        if self.type == VOLUME_TYPE_VOLUME:
            return hash(self.name)
        elif self.type == VOLUME_TYPE_BIND:
            return hash(self.source)
        else:
            raise ValueError("Uknown volume type: {}".format(self.type))


class RunningContainers:

    def __init__(self):
        all_containers = utils.list_containers()
        self.containers = []
        self.this_container = None
        self.backup_process_container = None

        # Find the container we are running in.
        # If we don't have this information we cannot continue
        for container_data in all_containers:
            if container_data.get('Id').startswith(os.environ['HOSTNAME']):
                self.this_container = Container(container_data)

        if not self.this_container:
            raise ValueError("Cannot find metadata for backup container")

        # Gather all containers in the current compose setup
        for container_data in all_containers:
            container = Container(container_data)

            # Detect running backup process container
            if container.is_backup_process_container:
                self.backup_process_container = container

            # Detect containers beloging to the current compose setup
            if container.project_name == self.this_container.project_name and not container.is_oneoff:
                if container.id != self.this_container.id:
                    self.containers.append(container)

    @property
    def backup_process_running(self) -> bool:
        """Is the backup process container running?"""
        return self.backup_process_container is not None

    def get_service(self, name) -> Container:
        for container in self.containers:
            if container.service_name == name:
                return container

        return None
