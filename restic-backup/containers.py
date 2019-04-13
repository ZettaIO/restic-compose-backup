import os
import docker
import json

DOCKER_BASE_URL = os.environ.get('DOCKER_BASE_URL') or "unix://tmp/docker.sock"
VOLUME_TYPE_BIND = "bind"
VOLUME_TYPE_VOLUME = "volume"

class Container:

    def __init__(self, data):
        self.id = data.get('Id')
        self.names = data.get('Names')
        self.mounts = [Mount(mnt, container=self) for mnt in data.get('Mounts')]

    def to_dict(self):
        return {
            "Id": self.id,
            "Mounts": [mnt.data for mnt in self.mounts]
        }


class Mount:
    """Mount wrapper"""
    def __init__(self, data, container=None):
        self.data = data
        self._container = container

    @property
    def container(self):
        return self._container

    @property
    def type(self):
        return self.data.get('Type')

    @property
    def name(self):
        return self.data.get('Name')

    @property
    def source(self):
        return self.data.get('Source')

    @property
    def destination(self):
        return self.data.get('Destination')

    @property
    def driver(self):
        return self.data.get('Driver')

    @property
    def mode(self):
        return self.data.get('Mode')

    @property
    def rw(self):
        return self.data.get('RW')

    def mount_string(self):
        if self.type == VOLUME_TYPE_VOLUME:
            return "- {}:{}:ro".format(self.name.split('_')[-1], self.destination)
        elif self.type == VOLUME_TYPE_BIND:
            return "- {}:{}:ro".format(self.source, self.destination)
        else:
            raise ValueError("Uknown volume type: {}".format(self.type))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.data)

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
        client = docker.Client(base_url=DOCKER_BASE_URL)
        all_containers = client.containers()
        client.close()

        self.containers = []
        self.backup_container = None

        for entry in all_containers:
            if entry['Id'].startswith(os.environ['HOSTNAME']):
                self.backup_container = Container(entry)
            else:
                if entry['State'] == "running":
                    self.containers.append(Container(entry))

        if not self.backup_container:
            raise ValueError("Cannot find metadata for backup container")

    def backup_volumes(self):
        return self.backup_container.mounts

    def gen_volumes(self, volume_type):
        """Generator yielding volumes of a specific type"""
        for cont in self.containers:
            for mnt in cont.mounts:
                if mnt.type == volume_type:
                    yield mnt

    def volume_mounts(self):
        """Docker volumes"""
        return set(mnt for mnt in self.gen_volumes(VOLUME_TYPE_VOLUME))

    def bind_mounts(self):
        """Host mapped volumes"""
        return set(mnt for mnt in self.gen_volumes(VOLUME_TYPE_BIND))

    def print_all(self):
        print("Backup container:")
        print(json.dumps(self.backup_container.to_dict(), indent=2))

        print("All containers:")
        print(json.dumps([cnt.to_dict() for cnt in self.containers], indent=2))
