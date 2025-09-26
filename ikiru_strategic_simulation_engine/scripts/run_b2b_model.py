# -*- coding: utf-8 -*-
"""
Script to run the B2B Win Probability model.
"""
import pandas as pd
from pathlib import Path
from isse.models.b2b_win_probability import B2BWinProbabilityModel

def main():
    """
    Main function to execute the B2B win probability model pipeline.
    """
    processed_data_path = Path("data/processed/processed_b2b_pipeline.csv")
    if not processed_data_path.exists():
        print(f"Processed data not found at {processed_data_path}. Please run the data processing pipeline first.")
        return

    pipeline_df = pd.read_csv(processed_data_path)

    # Initialize and train the model
    b2b_model = B2BWinProbabilityModel(pipeline_df)
    
    print("Training B2B Win Probability Model...")
    accuracy, fitted_model = b2b_model.train_and_evaluate()
    print(f"Model trained. Evaluation accuracy: {accuracy:.2%}")

    # Example prediction on the first 5 leads
    print("\nPredicting win probability for the first 5 leads in the dataset:")
    sample_leads = pipeline_df.head(5)
    win_probabilities = fitted_model.predict_proba(sample_leads)

    for i, prob in enumerate(win_probabilities):
        print(f"  Lead {sample_leads.iloc[i]['lead_id']}: {prob:.2%}")


if __name__ == "__main__":
    main()
