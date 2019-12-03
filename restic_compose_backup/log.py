import logging
import os
import sys

logger = logging.getLogger('restic_compose_backup')
HOSTNAME = os.environ['HOSTNAME']

level = logging.INFO
logger.setLevel(level)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(level)
ch.setFormatter(logging.Formatter(f'%(asctime)s - {HOSTNAME} - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)
