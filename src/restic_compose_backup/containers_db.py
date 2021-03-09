import logging
from pathlib import Path

from restic_compose_backup.containers import Container
from restic_compose_backup.config import config, Config
from restic_compose_backup import (
    commands,
    restic,
)
from restic_compose_backup import utils

logger = logging.getLogger(__name__)

class MariadbContainer(Container):
    container_type = 'mariadb'

    def get_credentials(self) -> dict:
        """dict: get credentials for the service"""
        return {
            'host': self.hostname,
            'username': 'root',
            'password': self.get_config_env('MYSQL_ROOT_PASSWORD'),
            'port': "3306",
        }

    def ping(self) -> bool:
        """Check the availability of the service"""
        creds = self.get_credentials()

        return commands.ping_mariadb(
            creds['host'],
            creds['port'],
            creds['username'],
            creds['password']
        )

    def dump_command(self) -> list:
        """list: create a dump command restic and use to send data through stdin"""
        creds = self.get_credentials()
        destination = self.backup_destination_path()

        return [
            "mydumper",
            "--user",
            creds['username'],
            "--password",
            creds['password'],
            "--host",
            creds['host'],
            "--port",
            creds['port'],
            "--outputdir",
            f"{destination}",
            "--no-views",
            "--compress",
            "--verbose",
            "3"
        ]

    def backup(self):
        config = Config()
        destination = self.backup_destination_path()

        commands.run([
            "mkdir",
            "-p",
            f"{destination}"
        ])
        commands.run(self.dump_command())

        return restic.backup_files(
            config.repository,
            f"{destination}",
            tags=self.tags
        )

    def backup_destination_path(self) -> str:
        destination = Path("/databases")

        if utils.is_true(config.include_project_name):
            project_name = self.project_name
            if project_name != "":
                destination /= project_name

        destination /= self.service_name

        return destination


class MysqlContainer(Container):
    container_type = 'mysql'

    def get_credentials(self) -> dict:
        """dict: get credentials for the service"""
        return {
            'host': self.hostname,
            'username': 'root',
            'password': self.get_config_env('MYSQL_ROOT_PASSWORD'),
            'port': "3306",
        }

    def ping(self) -> bool:
        """Check the availability of the service"""
        creds = self.get_credentials()

        return commands.ping_mysql(
            creds['host'],
            creds['port'],
            creds['username'],
            creds['password']
        )

    def dump_command(self) -> list:
        """list: create a dump command restic and use to send data through stdin"""
        creds = self.get_credentials()
        destination = self.backup_destination_path()

        return [
            "mydumper",
            "--user",
            creds['username'],
            "--password",
            creds['password'],
            "--host",
            creds['host'],
            "--port",
            creds['port'],
            "--outputdir",
            f"{destination}",
            "--no-views",
            "--compress",
            "--verbose",
            "3"
        ]

    def backup(self):
        config = Config()
        destination = self.backup_destination_path()

        commands.run([
            "mkdir",
            "-p",
            f"{destination}"
        ])
        commands.run(self.dump_command())

        return restic.backup_files(
            config.repository,
            f"{destination}",
            tags=self.tags
        )

    def backup_destination_path(self) -> str:
        destination = Path("/databases")

        if utils.is_true(config.include_project_name):
            project_name = self.project_name
            if project_name != "":
                destination /= project_name

        destination /= self.service_name

        return destination


class PostgresContainer(Container):
    container_type = 'postgres'

    def get_credentials(self) -> dict:
        """dict: get credentials for the service"""
        return {
            'host': self.hostname,
            'username': self.get_config_env('POSTGRES_USER'),
            'password': self.get_config_env('POSTGRES_PASSWORD'),
            'port': "5432",
            'database': self.get_config_env('POSTGRES_DB'),
        }

    def ping(self) -> bool:
        """Check the availability of the service"""
        creds = self.get_credentials()
        return commands.ping_postgres(
            creds['host'],
            creds['port'],
            creds['username'],
            creds['password'],
        )

    def dump_command(self) -> list:
        """list: create a dump command restic and use to send data through stdin"""
        # NOTE: Backs up a single database from POSTGRES_DB env var
        creds = self.get_credentials()
        return [
            "pg_dump",
            f"--host={creds['host']}",
            f"--port={creds['port']}",
            f"--username={creds['username']}",
            creds['database'],
        ]

    def backup(self):
        config = Config()
        creds = self.get_credentials()

        with utils.environment('PGPASSWORD', creds['password']):
            return restic.backup_from_stdin(
                config.repository,
                self.backup_destination_path(),
                self.dump_command(),
                tags=self.tags
            )

    def backup_destination_path(self) -> str:
        destination = Path("/databases")

        if utils.is_true(config.include_project_name):
            project_name = self.project_name
            if project_name != "":
                destination /= project_name

        destination /= self.service_name
        destination /= f"{self.get_credentials()['database']}.sql"

        return destination
