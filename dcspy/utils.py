from logging import getLogger
from os import makedirs
from yaml import load, FullLoader, parser, dump

LOG = getLogger(__name__)
defaults_cfg = {'keyboard': 'G13', 'verbose': True, 'show_gui': True}


def load_cfg(filename) -> dict:
    """
    Load configuration form yaml filename.

    :param filename: path to yam file
    :return: configuration dict
    """
    cfg_dict = {}
    try:
        with open(file=filename, encoding='utf-8') as yaml_file:
            cfg_dict = load(yaml_file, Loader=FullLoader)
            if not isinstance(cfg_dict, dict):
                cfg_dict, old_dict = {}, cfg_dict
                raise AttributeError(f'Config is not a dict {type(old_dict)} value: **{old_dict}**')
    except (FileNotFoundError, parser.ParserError, AttributeError) as err:
        makedirs(name=filename.rpartition('/')[0], exist_ok=True)
        LOG.warning(f'{err.__class__.__name__}: {filename}. Default configuration will be used.')
        LOG.debug(f'{err}')
    return cfg_dict


def save_cfg(cfg_dict: dict, filename) -> None:
    """
    Update yaml file with dict.

    :param cfg_dict: configuration dict
    :param filename: path to yam file
    """
    curr_dict = load_cfg(filename)
    curr_dict.update(cfg_dict)
    with open(file=filename, mode='w', encoding='utf-8') as yaml_file:
        dump(curr_dict, yaml_file)
