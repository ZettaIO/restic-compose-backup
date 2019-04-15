import os


class Config:
    repository = os.environ['RESTIC_REPOSITORY']
    password = os.environ['RESTIC_PASSWORD']

    @classmethod
    def check(cls):
        if not cls.repository:
            raise ValueError("CONTAINER env var not set")

        if not cls.password:
            raise ValueError("PASSWORD env var not set")
