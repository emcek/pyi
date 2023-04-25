from logging import getLogger
from pathlib import Path
from PIL import ImageFont
from dcspy.log import config_logger
from dcspy.utils import load_cfg

default_yaml = Path(__file__).resolve().with_name('config.yaml')
config = load_cfg(filename=default_yaml)
ded_path = Path(__file__).resolve().with_name('falconded.ttf')
DED_FONT = ImageFont.truetype(str(ded_path), 25)
LCD_TYPES = {
    'G19': {'icon': 'G19.png'},
    'G13': {'icon': 'G13.png'},
}
LOG = getLogger(__name__)
config_logger(LOG, config['verbose'])
LOG.info(f'Configuration: {config} from: {default_yaml}')
