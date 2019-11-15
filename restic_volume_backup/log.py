import logging
import sys

logger = logging.getLogger('restic_volume_backup')

level = logging.INFO
logger.setLevel(level)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(level)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
# ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)
