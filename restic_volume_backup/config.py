import os


class Config:
    repository = os.environ['RESTIC_REPOSITORY']
    password = os.environ['RESTIC_PASSWORD']
    docker_base_url = os.environ.get('DOCKER_BASE_URL') or "unix://tmp/docker.sock"

    @classmethod
    def check(cls):
        if not cls.repository:
            raise ValueError("CONTAINER env var not set")

        if not cls.password:
            raise ValueError("PASSWORD env var not set")
