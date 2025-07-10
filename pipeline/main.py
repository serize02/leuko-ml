import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

import logging
import pandas as pd

from common import read_yaml
from data_ingestion import DataIngestor
from trainer import Trainer
from pathlib import Path

CONFIG_PATH = Path('configs/config.yaml')

logging_str = '[%(levelname)s : %(module)s: %(message)s]'
log_dir = 'logs'
log_filepath = os.path.join(log_dir, 'running_logs.log')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('leuko_ml_logger')

if __name__ == '__main__':
    config = read_yaml(CONFIG_PATH)

    DATA_ARTIFACT_PATH = config.data_artifact_path
    MODEL_OUTPUT_PATH = config.model_output_path
    TARGET_COLUMN = config.target_column

    logger.info("Starting data ingestion")
    ingestor = DataIngestor()
    ingestor.run()
    logger.info("Data ingestion completed")

    logger.info(f"Checking for dataset at: {DATA_ARTIFACT_PATH}")
    assert os.path.exists(DATA_ARTIFACT_PATH), f"Dataset not found at {DATA_ARTIFACT_PATH}"

    logger.info("Loading dataset")
    data = pd.read_csv(DATA_ARTIFACT_PATH)

    logger.info(f"Checking target column '{TARGET_COLUMN}'")
    assert TARGET_COLUMN in data.columns, f"Target column '{TARGET_COLUMN}' not found in dataset"

    logger.info("Starting model training")
    trainer = Trainer(data, TARGET_COLUMN, MODEL_OUTPUT_PATH)
    trainer.run()
    logger.info(f"Model training completed and saved to {MODEL_OUTPUT_PATH}")
