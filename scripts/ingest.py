import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pathlib import Path
from utils.common import read_yaml
from pipeline.data_ingestion import DataIngestor

if __name__ == "__main__":
    config = read_yaml(Path("configs/config.yaml"))

    ingestor = DataIngestor(
        wandb_project=config.wandb_project,
        wandb_artifact=config.wandb_artifact
    )
    ingestor.run()