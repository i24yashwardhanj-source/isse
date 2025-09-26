Ikiru Strategic Simulation Engine (ISSE)
The ISSE is a comprehensive, data-driven simulation engine designed to model, forecast, and optimize the business strategy for Project Ikiru Synergy.

Project Structure
/
|-- configs/
|   |-- data_mapping.yaml       # Configuration for data loading (Future use)
|-- data/
|   |-- raw/                    # Raw, immutable data files
|   |-- processed/              # Cleaned, analysis-ready data
|-- notebooks/
|   |-- 01-d2c-ltv-modeling.ipynb # Exploratory analysis and model prototyping
|-- src/
|   |-- isse/
|   |   |-- io/                 # Data loading and schema validation
|   |   |   |-- loaders.py
|   |   |   |-- schemas.py
|   |   |-- models/             # Core statistical and ML models
|   |   |   |-- d2c_ltv.py
|   |   |   |-- d2c_mmm.py
|   |   |   |-- b2b_win_probability.py
|   |   |   |-- logistics_optimization.py
|   |   |   |-- financial_simulation.py
|-- scripts/
|   |-- process_data.py         # Script to run the data pipeline
|   |-- run_ltv_model.py        # Script to run the LTV model
|-- requirements.txt            # Project dependencies
|-- Dockerfile                  # For containerization
|-- docker-compose.yml          # For multi-container orchestration

Setup and Installation
Clone the repository:

git clone <repository-url>
cd isse_project

Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

Running the Engine
The engine is composed of several modules that can be run via the scripts in the /scripts directory. Ensure you have placed your raw CSV files in the data/raw/ directory first.

Process Raw Data:
This script runs the robust data loader, which cleans all raw data files and saves the processed output to /data/processed/.

python scripts/process_data.py

Run a Specific Model:
Each model has a dedicated script that loads the processed data and runs the corresponding analysis. For example, to run the D2C LTV model:

python scripts/run_ltv_model.py
