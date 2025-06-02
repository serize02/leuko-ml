import pandas as pd
import numpy as np
import pickle as pkl
import shap
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

def generate(model_path, data_path):

    data = pd.read_csv(data_path)
    X, y = data.drop('discharge_status', axis=1), data['discharge_status']

    apache_score_avg = np.mean(data['apache_score'])
    leuko_avg = np.mean(data['leuko_glycemic_index'])

    with open(model_path, 'rb') as file:
        model = pkl.load(file)

    explainer = shap.KernelExplainer(lambda x: model.predict_proba(x)[:, 1], X)
    shap_values = explainer(X)

    y_preds = model.predict(X)

    prompts = []

    for i, sv in tqdm(enumerate(shap_values), desc='XAI-prompts'):

        values = sv.values
        input_values = sv.data
        expected_value = sv.base_values

        apache_ = f'(apache_score, {input_values[0]}, {values[0]}, {apache_score_avg})'
        leuko_ = f'(leuko_glycemic_index, {input_values[1]}, {values[1]}, {leuko_avg})'

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