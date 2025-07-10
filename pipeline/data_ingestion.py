import os
import wandb
import logging

logger = logging.getLogger(__name__)

class DataIngestor:

    def __init__(self, wandb_project: str, wandb_artifact: str):
        self.wandb_project = wandb_project
        self.wandb_artifact = wandb_artifact
        self.artifact_path = None

    def run(self):
        logger.info("Starting data ingestion with wandb artifact")
        run = wandb.init(project=self.wandb_project)
        artifact = run.use_artifact(self.wandb_artifact, type='dataset')
        artifact_dir = artifact.download()
        wandb.finish()

        logger.info(f"Artifact downloaded to: {artifact_dir}")
        expected_file = os.path.join(artifact_dir, 'new_data.csv')
        assert os.path.isfile(expected_file)
        self.artifact_path = expected_file
