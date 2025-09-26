# Makefile for Ikiru Strategic Simulation Engine (ISSE)

# Default command
all: help

# Build the Docker environment
build:
	@echo "Building the ISSE Docker environment..."
	docker-compose build

# Start the services in detached mode
up:
	@echo "Starting ISSE services..."
	docker-compose up -d

# Stop the services
down:
	@echo "Stopping ISSE services..."
	docker-compose down

# Access the application container's shell
shell:
	@echo "Accessing the ISSE application shell..."
	docker-compose exec isse_app bash

# Run the data processing pipeline
process-data:
	@echo "Running the data processing pipeline..."
	docker-compose exec isse_app python -m scripts.process_data

# Run the D2C LTV model
run-ltv-model:
	@echo "Running D2C Customer Lifetime Value (LTV) model..."
	docker-compose exec isse_app python -m scripts.run_ltv_model

# Run the D2C Marketing Mix Model
run-mmm-model:
	@echo "Running D2C Marketing Mix Model (MMM)..."
	docker-compose exec isse_app python -m scripts.run_mmm_model

# Run the B2B Win Probability Model
run-b2b-model:
	@echo "Running B2B Win Probability Model..."
	docker-compose exec isse_app python -m scripts.run_b2b_model

# Run the Logistics Optimization Model
run-logistics-model:
	@echo "Running Logistics Optimization Model for Mumbai..."
	docker-compose exec isse_app python -m scripts.run_logistics_model

# Run the Final Integrated Financial Simulation
run-final-simulation:
	@echo "Running the Final Integrated Financial Simulation..."
	docker-compose exec isse_app python -m scripts.run_financial_simulation

# Help command to display available commands
help:
	@echo ""
	@echo "Available commands for the ISSE project:"
	@echo "-----------------------------------------"
	@echo "make build                - Builds the Docker environment for the first time."
	@echo "make up                   - Starts the Docker services in the background."
	@echo "make down                 - Stops the Docker services."
	@echo "make shell                - Access the command line inside the running container."
	@echo "make process-data         - Runs the entire data cleaning and preparation pipeline."
	@echo "make run-ltv-model        - Runs the D2C Customer LTV model."
	@echo "make run-mmm-model        - Runs the D2C Marketing Mix Model."
	@echo "make run-b2b-model        - Runs the B2B Win Probability model."
	@echo "make run-logistics-model  - Runs the Logistics Optimization simulation."
	@echo "make run-final-simulation - Runs the complete, integrated financial forecast."
	@echo ""

