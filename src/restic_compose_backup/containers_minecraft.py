import os
import logging

from pathlib import Path

from restic_compose_backup.containers import Container
from restic_compose_backup.config import config, Config
from restic_compose_backup import (
    commands,
    restic,
    rcon
)
from restic_compose_backup import utils

logger = logging.getLogger(__name__)


class MinecraftContainer(Container):
    container_type = 'minecraft'

    def get_credentials(self) -> dict:
        """dict: get credentials for the service"""
        return {
            'host': self.hostname,
            'password': self.get_config_env('RCON_PASSWORD'),
            'port': self.get_config_env('RCON_PORT'),
        }

    def prepare_mc_backup(self) -> bool:
        creds = self.get_credentials()

        with utils.environment('RCON_PASSWORD', creds['password']):
            rcon.save_off(creds['host'], creds['port'])
            rcon.save_all(creds['host'], creds['port'])
            rcon.sync(creds['host'], creds['port'])
            return True

    def ping(self) -> bool:
        """Check the availability of the service"""
        creds = self.get_credentials()

        try:
            logger.debug("[rcon-cli] checking if minecraft server %s is online...", self.service_name)
            with utils.environment('RCON_PASSWORD', creds['password']):
                return rcon.is_online(
                    creds['host'],
                    creds['port']
                )
        except Exception as ex:
            logger.error('[rcon-cli] unable to contact minecraft server %s', self.service_name)
            return 1

    def backup(self) -> bool:
        config = Config()
        creds = self.get_credentials()

        errors = False
        with utils.environment('RCON_PASSWORD', creds['password']):
            try:
                # turn off auto-save and sync all data to the disk before backing up worlds
                self.prepare_mc_backup()

                for mount in self.filter_mounts():
                    backup_data = self.get_volume_backup_destination(mount, '/minecraft')
                    logger.info('Backing up %s', mount.source)
                    vol_result = restic.backup_files(config.repository, source=backup_data, tags=self.tags)
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