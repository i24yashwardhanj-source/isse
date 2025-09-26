# -*- coding: utf-8 -*-
"""
B2B Project Win Probability Prediction Module.

--- AUDIT v1 UPGRADE: Replaced RandomForest with LogisticRegression. ---
This provides a more stable and interpretable baseline model for predicting
win probability, which can serve as a robust proxy for the full Bayesian model.
"""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from typing import Tuple

class B2BWinProbabilityModel:
    """
    A class to train a model to predict the probability of winning a B2B project.
    """
    def __init__(self, pipeline_df: pd.DataFrame):
        self.pipeline_df = pipeline_df
        self.features = ['lead_source', 'project_type', 'potential_value_inr']
        self.target = 'is_won'
        
        # Define preprocessing steps
        categorical_features = ['lead_source', 'project_type']
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ],
            remainder='passthrough'
        )
        
        self.model_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression(random_state=42, class_weight='balanced'))
        ])

    def train_and_evaluate(self) -> Tuple[float, 'B2BWinProbabilityModel']:
        """
        Trains the model and evaluates its accuracy.
        """
        X = self.pipeline_df[self.features]
        y = self.pipeline_df[self.target]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model_pipeline.fit(X_train, y_train)
        accuracy = self.model_pipeline.score(X_test, y_test)
        
        return accuracy, self

    def predict_proba(self, new_leads_df: pd.DataFrame) -> pd.DataFrame:
        """
        Predicts the win probability for new leads.
        """
        probabilities = self.model_pipeline.predict_proba(new_leads_df[self.features])
        # Return probability of the 'won' class (class 1)
        return probabilities[:, 1]

