from restic_volume_backup.containers import Container
from restic_volume_backup import (
    commands,
    restic,
)


class MariadbContainer(Container):
    container_type = 'mariadb'

    def get_credentials(self) -> dict:
        """dict: get credentials for the service"""
        return {
            'host': self.hostname,
            'username': self.get_config_env('MYSQL_USER'),
            'password': self.get_config_env('MYSQL_PASSWORD'),
            'port': "3306",
        }

    def ping(self) -> bool:
        """Check the availability of the service"""
        creds = self.get_credentials()
        return commands.ping_mysql(
            creds['host'],
            creds['port'],
            creds['username'],
            creds['password'],
        )

    def dump_command(self) -> list:
        """list: create a dump command restic and use to send data through stdin"""
        creds = self.get_credentials()
        return [
            "mysqldump",
            f"--host={creds['host']}",
            f"--port={creds['port']}",
            f"--user={creds['username']}",
            f"--password={creds['password']}",
            "--all-databases",
        ]

    def backup(self):
        return restic.backup_from_stdin(
            f'/backup/{self.service_name}',
            self.dump_command(),
        )


class MysqlContainer(Container):
    container_type = 'mysql'

    def get_credentials(self) -> dict:
        """dict: get credentials for the service"""
        return {
            'host': self.hostname,
            'username': self.get_config_env('MYSQL_USER'),
            'password': self.get_config_env('MYSQL_PASSWORD'),
            'port': "3306",
        }

    def ping(self) -> bool:
        """Check the availability of the service"""
        creds = self.get_credentials()
        return commands.ping_mysql(
            creds['host'],
            creds['port'],
            creds['username'],
            creds['password'],
        )

    def dump_command(self) -> list:
        """list: create a dump command restic and use to send data through stdin"""
        raise NotImplementedError("Base container class don't implement this")

    def backup(self):
        print("SKIPPING")


class PostgresContainer(Container):
    container_type = 'postgres'

    def get_credentials(self) -> dict:
        """dict: get credentials for the service"""
        return {
            'host': self.hostname,
            'username': self.get_config_env('POSTGRES_USER'),
            'password': self.get_config_env('POSTGRES_PASSWORD'),
            'port': "5432",
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
        raise NotImplementedError("Base container class don't implement this")

    def backup(self):
        print("SKIPPING")
