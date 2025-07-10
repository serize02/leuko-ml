import os
import wandb

class DataIngestor:

    def __init__(self):
        pass

    def run(self):
        run = wandb.init(project='leuko-ml')
        artifact = run.use_artifact(
            'ernestoserize-constructor-university/leuko-ml/acute-stroke-selected:v2',
            type='dataset'
        )
        artifact_dir = artifact.download()
        wandb.finish()
        assert os.path.exists(artifact_dir)
        expected_file = os.path.join(artifact_dir, 'new_data.csv')
        assert os.path.isfile(expected_file)