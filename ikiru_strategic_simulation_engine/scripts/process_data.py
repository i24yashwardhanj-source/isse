# -*- coding: utf-8 -*-
"""
Main script to execute the full data loading and validation pipeline.
"""
import os
from isse.io.loaders import DataLoader

def main():
    """
    Main function to run the data loader and save processed files.
    """
    RAW_DATA_DIR = "data/raw"
    PROCESSED_DATA_DIR = "data/processed"

    # Ensure the processed data directory exists
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    loader = DataLoader(raw_data_path=RAW_DATA_DIR)
    dataframes = loader.load_and_validate_all()

    if not dataframes:
        print("No dataframes were loaded. Exiting.")
        return

    for name, df in dataframes.items():
        output_path = os.path.join(PROCESSED_DATA_DIR, f"processed_{name}.csv")
        df.to_csv(output_path, index=False)
        print(f"Saved processed data for '{name}' to {output_path}")


if __name__ == "__main__":
    main()
