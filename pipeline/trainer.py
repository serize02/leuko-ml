import os
import joblib
import warnings

import numpy as np
import pandas as pd

from sklearn.metrics import make_scorer, fbeta_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, GridSearchCV

warnings.filterwarnings("ignore", message="invalid value encountered in cast", category=RuntimeWarning)

class Trainer:

    def __init__(self, data, target, output_path):
        assert target in data.columns
        assert output_path.endswith('.joblib')
        assert len(data) > 0

        self.X = data.drop(columns=[target])
        self.y = data[target]

        assert self.X.select_dtypes(exclude='number').empty
        assert np.isfinite(self.X.to_numpy()).all()
        assert not self.X.isnull().any().any()
        assert len(np.unique(self.y)) >= 2

        self.scorer = make_scorer(fbeta_score, beta=2, pos_label=1, zero_division=1)

        self.clf = Pipeline(steps=[
            ('scaler', StandardScaler()),
            ('estimator', KNeighborsClassifier())
        ])

        self.skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)

        self.params = {
            'estimator__n_neighbors': [3, 5, 7, 9],
            'estimator__metric': ['euclidean', 'manhattan', 'minkowski'],
            'estimator__p': [1, 2, 3],
            'estimator__leaf_size': [20, 30, 40, 50],
        }

        self.grid = GridSearchCV(
            self.clf,
            self.params,
            scoring=self.scorer,
            cv=self.skf,
            error_score='raise'
        )

        self.output_path = output_path

    def run(self):
        assert self.X.shape[0] == self.y.shape[0]
        self.grid.fit(self.X, self.y)
        joblib.dump(self.grid.best_estimator_, self.output_path)
        assert os.path.exists(self.output_path)