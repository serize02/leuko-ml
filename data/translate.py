import pandas as pd
import json

df = pd.read_csv('raw/data.csv')

with open('column_translation.json', 'r', encoding='utf-8') as f:
    column_mapping = json.load(f)

df_renamed = df.rename(columns=column_mapping)

df_renamed.to_csv('raw/data.csv', index=False)