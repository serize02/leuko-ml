import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pathlib import Path
import pandas as pd
from utils.common import read_yaml
from pipeline.trainer import Trainer

if __name__ == "__main__":
    config = read_yaml(Path("configs/config.yaml"))

    data_path = Path(config.data_artifact_path)
    data = pd.read_csv(data_path)

    trainer = Trainer(
        data=data,
        target=config.target_column,
        output_path=config.model_output_path
    )
    trainer.run()