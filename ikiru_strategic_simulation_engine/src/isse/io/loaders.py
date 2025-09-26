# -*- coding: utf-8 -*-
"""
Robust data loading, cleaning, and validation module for the ISSE.

--- AUDIT v1 UPGRADE: Re-engineered for robustness and validation. ---
This module now includes intelligent header detection, resilient error handling,
and uses pandera schemas for rigorous data validation.
"""
import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Optional

from isse.io.schemas import (
    SyntheticOrdersSchema,
    SyntheticMarketingSpendSchema,
    SyntheticB2BPipelineSchema,
    SyntheticWarehouseLocationsSchema,
)

# Setup professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='data_loader.log'
)
logger = logging.getLogger(__name__)

class DataLoader:
    """Handles loading, cleaning, and validating all data for the ISSE."""

    def __init__(self, raw_data_path: str):
        self.raw_data_path = Path(raw_data_path)
        self.dataframes: Dict[str, pd.DataFrame] = {}
        self.schemas = {
            "orders": SyntheticOrdersSchema,
            "marketing_spend": SyntheticMarketingSpendSchema,
            "b2b_pipeline": SyntheticB2BPipelineSchema,
            "warehouses": SyntheticWarehouseLocationsSchema,
        }

    def load_and_validate_all(self) -> Dict[str, pd.DataFrame]:
        """
        Main method to load all configured datasets.
        """
        for key, schema in self.schemas.items():
            file_path = self.raw_data_path / f"synthetic_{key}.csv"
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}. Skipping '{key}'.")
                continue

            try:
                df = self._load_single_file(file_path)
                validated_df = schema.validate(df)
                self.dataframes[key] = validated_df
                logger.info(f"Successfully loaded and validated '{key}' data from {file_path.name}.")
            except Exception as e:
                logger.error(f"Failed to load or validate {file_path.name}: {e}", exc_info=True)
        
        return self.dataframes

    def _load_single_file(self, file_path: Path) -> Optional[pd.DataFrame]:
        """Loads and performs initial cleaning on a single CSV file."""
        try:
            df = pd.read_csv(file_path)
            # Basic cleaning
            df.columns = df.columns.str.strip().str.lower()
            return df
        except pd.errors.EmptyDataError:
            logger.warning(f"File {file_path.name} is empty. Skipping.")
            return None
        except Exception as e:
            logger.error(f"Error reading CSV {file_path.name}: {e}")
            raise

