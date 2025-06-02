import json
from utils.prompt import generate

model_path = 'artifacts/knn:v0/knn.pkl'
data_path = 'artifacts/acute-stroke-selected:v2/new_data.csv'

prompts = generate(model_path, data_path)

with open("outputs/meta-prompts.json", "w") as f:
    json.dump(prompts, f, indent=2)