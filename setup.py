from setuptools import setup, find_namespace_packages

setup(
    name="restic-volume-backup",
    url="https://github.com/ZettaIO/restic-volume-backup",
    version="1.0.0",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    packages=find_namespace_packages(include=['restic_volume_backup']),
    install_requires=[
        'docker==3.7.2',
    ],
    entry_points={'console_scripts': [
        'restic-volume-backup = restic_volume_backup.cli:main',
    ]},
)
