import os
import docker


client = docker.Client(base_url=DOCKER_BASE_URL)

container = client.containers.run(
    'image',
    'command',
    labels={"restic-volume-backup.process": True},
    auto_remove=True,
    remove=True,
    detach=True,
    environment={
        'test1': 'value1',
        'test2': 'value2',
    },
    volumes={
        '/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
        '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'},
    },
    working_dir=os.getcwd(),
)

# Pull logs and exist status of container
