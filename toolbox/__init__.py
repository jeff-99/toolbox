__author__ = 'Jeffrey Slort'
__email__ = 'j_slort@hotmail.com'
__version__ = '0.3.9'

import logging
from logging import FileHandler

logger = logging.getLogger(__name__)
handler = FileHandler('/home/jeff/.toolbox/toolbox.log', 'w','utf-8')
logger.addHandler(handler)

logger.warning('starting')git