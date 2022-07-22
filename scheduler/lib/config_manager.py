from configparser import ConfigParser
from pathlib import Path

config_file = 'scheduler/config.ini'
config = ConfigParser()
config.read(Path(config_file))


def get_config_value(header, key):
    return config[header][key]