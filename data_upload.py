import wandb
wandb.login()

import pandas as pd

from utils.common import read_yaml
from pathlib import Path

config = read_yaml(Path('configs/config.yaml'))['data']
path = config['local_path']

data = pd.read_csv(path)

wandb.init(
    project='leuko-ml',
    name='data-upload',
    tags=['raw', 'cleaned']
)

artifact = wandb.Artifact(
    name='acute-stroke-clinical-data',
    type='dataset',
    metadata={
        'source': 'hospital internal .csv export',
        'num_samples': len(data),
        'num_features': len(data.columns),
        'language': 'english',
    },
)

artifact.add_file('data/data.csv')

wandb.log_artifact(artifact)

wandb.finish()