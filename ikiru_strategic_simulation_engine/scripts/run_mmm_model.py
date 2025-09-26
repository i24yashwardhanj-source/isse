# -*- coding: utf-8 -*-
"""
Script to run the D2C Marketing Mix Model (MMM).
"""
import pandas as pd
from pathlib import Path
from isse.models.d2c_mmm import MarketingMixModel

def main():
    """
    Main function to execute the D2C MMM pipeline.
    """
    # For MMM, we need both spend and a target variable (e.g., acquisitions)
    spend_path = Path("data/processed/processed_marketing_spend.csv")
    orders_path = Path("data/processed/processed_orders.csv")

    if not spend_path.exists() or not orders_path.exists():
        print("Processed marketing spend or orders data not found. Please run the data processing pipeline first.")
        return

    spend_df = pd.read_csv(spend_path, parse_dates=['date'], index_col='date')
    orders_df = pd.read_csv(orders_path, parse_dates=['order_date'])
    
    # Aggregate orders to weekly acquisitions to match spend data
    acquisitions = orders_df.set_index('order_date').resample('W-MON').size().rename('acquisitions')
    
    # Align data
    aligned_df = spend_df.join(acquisitions, how='inner')
    
    spend_cols = ['social_media', 'search', 'influencer']
    target_col = 'acquisitions'

    mmm = MarketingMixModel(aligned_df[spend_cols], aligned_df[target_col])

    # These hyperparameters would typically be found through optimization/calibration
    decay_rates = {'social_media': 0.5, 'search': 0.2, 'influencer': 0.6}
    saturation_alphas = {'social_media': 0.01, 'search': 0.005, 'influencer': 0.015}

    print("Fitting Marketing Mix Model...")
    mmm.fit(decay_rates, saturation_alphas)
    print("Model fitting complete.")
    
    coefficients = mmm.get_coefficients()
    print("\nFitted Channel Coefficients (Contribution):")
    for channel, coef in coefficients.items():
        print(f"  {channel}: {coef:.2f}")


if __name__ == "__main__":
    main()
