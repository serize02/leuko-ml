import gdown
from utils.common import read_yaml
from pathlib import Path

config = read_yaml(Path('configs/config.yaml'))['data']

drive = config['drive']
path = config['path']

gdown.download(drive, path)