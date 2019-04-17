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
        self.id = data.get('Id')
        self.state = data.get('State')
        self.image = data.get('Image')
        self.labels = data.get('Labels', {})
        self.names = data.get('Names', [])
        self.mounts = [Mount(mnt, container=self) for mnt in data.get('Mounts')]

        self.include = self._parse_pattern(self.labels.get('restic-volume-backup.include'))
        self.exclude = self._parse_pattern(self.labels.get('restic-volume-backup.exclude'))

    def _parse_pattern(self, value):
        if not value:
            return None

        if type(value) is not str:
            return None

        value = value.strip()
        if len(value) == 0:
            return None

        return value.split(',')

    @property
    def backup_enabled(self):
        """Is backup enabled for this container?"""
        return self.labels.get('restic-volume-backup.enabled') == 'True'

    @property
    def is_backup_process_container(self):
        """Is this container the running backup process?"""
        return self.labels.get('restic-volume-backup.backup_process') == 'True'

    @property
    def is_running(self):
        """Is the container running?"""
        return self.state == 'running'

    @property
    def service_name(self):
        """Name of the container/service"""
        return self.labels.get('com.docker.compose.service', '')

    @property
    def project_name(self):
        """Name of the compose setup"""
        return self.labels.get('com.docker.compose.project', {})

    @property
    def is_oneoff(self):
        """Was this container started with run command?"""
        return self.labels.get('com.docker.compose.oneoff', 'False') == 'True'

    def filter_mounts(self):
        """Get all mounts for this container matching include/exclude filters"""
        filtered = []
        if self.include:
            for mount in self.mounts:
                for pattern in self.include:
                    if pattern in mount.source:
                        break
                else:
                    continue

                filtered.append(mount)

        elif self.exclude:
            for mount in self.mounts:
                for pattern in self.exclude:
                    if pattern in mount.source:
                        break
                else:
                    filtered.append(mount)
        else:
            return self.mounts

        return filtered

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

    # def gen_volumes(self, volume_type):
    #     """Generator yielding volumes of a specific type"""
    #     for cont in self.containers:
    #         for mnt in cont.mounts:
    #             if mnt.type == volume_type:
    #                 yield mnt

    # def volume_mounts(self):
    #     """Docker volumes"""
    #     return set(mnt for mnt in self.gen_volumes(VOLUME_TYPE_VOLUME))

    # def bind_mounts(self):
    #     """Host mapped volumes"""
    #     return set(mnt for mnt in self.gen_volumes(VOLUME_TYPE_BIND))

    @property
    def backup_process_running(self) -> bool:
        """Is the backup process container running?"""
        return self.backup_process_container is not None

    def get_service(self, name) -> Container:
        for container in self.containers:
            if container.service_name == name:
                return container

        return None
