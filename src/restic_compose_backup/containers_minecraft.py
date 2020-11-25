from pathlib import Path

from restic_compose_backup.containers import Container
from restic_compose_backup.config import config, Config
from restic_compose_backup import (
    commands,
    restic,
    rcon
)
from restic_compose_backup import utils


class MinecraftContainer(Container):
    container_type = 'minecraft'

    def get_credentials(self) -> dict:
        """dict: get credentials for the service"""
        return {
            'host': self.hostname,
            'password': self.get_config_env('RCON_PASSWORD'),
            'port': self.get_config_env('RCON_PORT'),
        }

    def ping(self) -> bool:
        """Check the availability of the service"""
        creds = self.get_credentials()

        logger.debug("[rcon-cli] checking if minecraft server %s is online...", self.service_name)
        with utils.environment('RCON_PASSWORD', creds['password']):
            return rcon.is_online(
                creds['host'],
                creds['port']
            )

    def backup(self) -> bool:
        config = Config()
        creds = self.get_credentials()

        errors = False
        with utils.environment('RCON_PASSWORD', creds['password']):
            try:
                # turn off auto-save and sync all data to the disk before backing up worlds
                prepare_mc_backup()
                for mount in container.filter_mounts():
                    backup_data = container.get_volume_backup_destination(mount, '/volumes')
                        logger.info('Backing up %s', mount.source)
                        vol_result = restic.backup_files(config.repository, source=backup_data)
                        logger.debug('Minecraft backup exit code: %s', vol_result)
                        if vol_result != 0:
                            logger.error('Minecraft backup exited with non-zero code: %s', vol_result)
                            errors = True
            except Exception as ex:
                logger.error('Exception raised during minecraft backup')
                logger.exception(ex)
                errors = True

            # always always turn saving back on
            rcon.save_on(creds['host'], creds['port'])

        return errors

    
    def prepare_mc_backup():
        creds = self.get_credentials()

        with utils.environment('RCON_PASSWORD', creds['password']):
            rcon.save_off(creds['host'], creds['port'])
            rcon.save_all(creds['host'], creds['port'])
            rcon.sync(creds['host'], creds['port'])