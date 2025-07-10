import shap
import joblib
import warnings
import pandas as pd
import numpy as np
from tqdm import tqdm
import logging

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class PromptGenerator:
    def __init__(self, model_path: str, data_path: str):
        self.model_path = model_path
        self.data_path = data_path

        logger.info("Loading data and model")
        self.data = pd.read_csv(self.data_path)
        self.X = self.data.drop(columns=['discharge_status'])
        self.y = self.data['discharge_status']
        self.model = joblib.load(self.model_path)

        self.apache_score_avg = float(np.mean(self.data['apache_score']))
        self.leuko_avg = float(np.mean(self.data['leuko_glycemic_index']))

    def run(self):
        logger.info("Initializing SHAP explainer")
        explainer = shap.KernelExplainer(lambda x: self.model.predict_proba(x)[:, 1], self.X)
        shap_values = explainer(self.X)

        y_preds = self.model.predict(self.X)
        prompts = []

        logger.info("Generating prompts")
        for i, sv in tqdm(enumerate(shap_values), desc='XAI-prompts'):
            values = sv.values
            input_values = sv.data
            expected_value = sv.base_values

            apache_ = f'(apache_score, {input_values[0]}, {values[0]}, {self.apache_score_avg})'
            leuko_ = f'(leuko_glycemic_index, {input_values[1]}, {values[1]}, {self.leuko_avg})'

            prompt = f"""
                You are helping users understand an ML model's prediction. The model predicts survival chance of patients with acute stroke. A higher model output means more survival chance. 

                The **expected value of the model's output** is {expected_value}. This is the baseline risk for all patients.

                I will give you feature contribution explanations, generated using SHAP, in (feature, feature_value, contribution, average_feature_value) format.
                Convert the explanations in simple narratives. Do not use more tokens than necessary.
                
                {apache_}
                {leuko_}
            """

            prompts.append({
                'id': i,
                'apache_score': float(input_values[0]),
                'leuko_glycemic_index': float(input_values[1]),
                'prediction': float(y_preds[i]),
                'prompt': prompt.strip(),
            })

        return prompts
