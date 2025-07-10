import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from pathlib import Path
from utils.common import read_yaml
from pipeline.prompt_generator import PromptGenerator

if __name__ == "__main__":
    config = read_yaml(Path("configs/config.yaml"))

    model_path = config.model_output_path
    data_path = config.data_artifact_path
    output_path = config.meta_prompt_output

    assert os.path.isfile(model_path), f"Model not found: {model_path}"
    assert os.path.isfile(data_path), f"Data not found: {data_path}"

    generator = PromptGenerator(model_path, data_path)
    prompts = generator.run()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(prompts, f, indent=2)

    assert os.path.isfile(output_path), f"Failed to save prompts to: {output_path}"
