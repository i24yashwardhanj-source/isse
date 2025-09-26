# -*- coding: utf-8 -*-
"""
D2C Marketing Mix Modeling (MMM) Module.

--- AUDIT v1 UPGRADE: Re-implemented with Adstock and Saturation. ---
This module now correctly implements the essential non-linear transformations
required for a modern MMM, bringing it in line with our blueprint.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict

class MarketingMixModel:
    """
    A class to build and analyze a Marketing Mix Model with carryover and
    diminishing returns effects.
    """
    def __init__(self, spend_df: pd.DataFrame, target_series: pd.Series):
        self.spend_df = spend_df
        self.target_series = target_series
        self.model = LinearRegression()

    def _apply_adstock(self, series: pd.Series, decay_rate: float) -> np.ndarray:
        """Applies the geometric adstock transformation."""
        adstock_series = np.zeros_like(series, dtype=float)
        adstock_series[0] = series.iloc[0]
        for i in range(1, len(series)):
            adstock_series[i] = series.iloc[i] + decay_rate * adstock_series[i-1]
        return adstock_series

    def _apply_saturation(self, series: np.ndarray, alpha: float) -> np.ndarray:
        """Applies the Hill saturation function."""
        return 1 - np.exp(-alpha * series)

    def fit(self, decay_rates: Dict[str, float], saturation_alphas: Dict[str, float]):
        """
        Transforms the spend data and fits the linear regression model.
        """
        transformed_features = pd.DataFrame(index=self.spend_df.index)
        for channel, decay in decay_rates.items():
            adstocked = self._apply_adstock(self.spend_df[channel], decay)
            saturated = self._apply_saturation(adstocked, saturation_alphas[channel])
            transformed_features[f'{channel}_transformed'] = saturated

        self.model.fit(transformed_features, self.target_series)
        return self

    def get_coefficients(self) -> Dict[str, float]:
        """Returns the fitted coefficients for each channel."""
        return {
            channel: coef 
            for channel, coef in zip(self.spend_df.columns, self.model.coef_)
        }

