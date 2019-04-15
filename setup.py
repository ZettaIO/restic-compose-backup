from setuptools import setup, find_namespace_packages

setup(
    name="restic-volume-backup",
    url="https://github.com/ZettaIO/restic-volume-backup",
    version="1.0.0",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    packages=find_namespace_packages(include=['restic_volume_backup']),
    install_requires=[
        'docker-py==1.10.6',
    ],
)
