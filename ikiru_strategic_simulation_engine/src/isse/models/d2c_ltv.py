# -*- coding: utf-8 -*-
"""
D2C Customer Lifetime Value (LTV) Prediction Module.

This module implements the Pareto/NBD model using the 'lifetimes' library
to predict the future purchase behavior and LTV of D2C customers, directly
aligning with our mathematical blueprint.
"""
import pandas as pd
from lifetimes import ParetoNBDFitter
from lifetimes.utils import summary_data_from_transaction_data
from typing import Optional

class D2CLTVModel:
    """
    A class to train a Pareto/NBD model and predict D2C customer LTV.
    """
    def __init__(self, penalizer_coef: float = 0.001):
        """
        Initializes the Pareto/NBD model fitter.
        
        Args:
            penalizer_coef: The coefficient for the L2 penalty term to prevent
                          overfitting.
        """
        self.model = ParetoNBDFitter(penalizer_coef=penalizer_coef)
        self.summary_data: Optional[pd.DataFrame] = None

    def fit(self, orders_df: pd.DataFrame) -> 'D2CLTVModel':
        """
        Trains the model on customer transaction data.

        Args:
            orders_df: A DataFrame with customer_id, order_date, and revenue_inr.

        Returns:
            The fitted model instance.
        """
        self.summary_data = summary_data_from_transaction_data(
            orders_df,
            customer_id_col='customer_id',
            datetime_col='order_date',
            monetary_value_col='revenue_inr',
            observation_period_end=orders_df['order_date'].max(),
            freq='D'
        )
        self.model.fit(
            self.summary_data['frequency'], 
            self.summary_data['recency'], 
            self.summary_data['T']
        )
        return self

    def predict_future_purchases(self, t_days: int = 365) -> Optional[pd.DataFrame]:
        """
        Predicts the number of purchases for each customer in a future period.

        Args:
            t_days: The number of future days to predict for.

        Returns:
            A DataFrame with customer IDs and their predicted number of purchases.
        """
        if self.summary_data is None:
            raise RuntimeError("Model has not been fitted yet. Call .fit() first.")
            
        summary = self.summary_data
        summary['predicted_purchases'] = self.model.predict(
            t=t_days,
            frequency=summary['frequency'],
            recency=summary['recency'],
            T=summary['T']
        )
        return summary[['predicted_purchases']]

