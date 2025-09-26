# -*- coding: utf-8 -*-
"""
Main entry point for the Ikiru Strategic Simulation Engine (ISSE).

This script provides a command-line interface (CLI) to run all modules
of the ISSE, from data processing to running the final financial simulation.
"""
import click
import os

# Dynamically add the src directory to the python path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from isse.scripts import (
    process_data,
    run_b2b_model,
    run_d2c_ltv_model,
    run_d2c_mmm_model,
    run_financial_simulation,
    run_logistics_model,
)

@click.group()
def isse_cli():
    """
    Ikiru Strategic Simulation Engine (ISSE)
    
    A command-line tool to run various strategic models and simulations.
    """
    pass

@isse_cli.command()
def process_data_pipeline():
    """Runs the full data processing and validation pipeline."""
    click.echo("Starting data processing pipeline...")
    process_data.main()
    click.echo("Data processing pipeline finished successfully.")

@isse_cli.command()
def run_ltv():
    """Runs the D2C Customer Lifetime Value (LTV) model."""
    click.echo("Running D2C LTV model...")
    run_d2c_ltv_model.main()
    click.echo("D2C LTV model run finished.")

@isse_cli.command()
def run_mmm():
    """Runs the D2C Marketing Mix Model (MMM)."""
    click.echo("Running D2C Marketing Mix Model...")
    run_d2c_mmm_model.main()
    click.echo("D2C MMM run finished.")

@isse_cli.command()
def run_b2b_win_prob():
    """Runs the B2B Win Probability model."""
    click.echo("Running B2B Win Probability model...")
    run_b2b_model.main()
    click.echo("B2B Win Probability model run finished.")

@isse_cli.command()
def run_logistics_opt():
    """Runs the logistics route optimization model."""
    click.echo("Running logistics route optimization...")
    run_logistics_model.main()
    click.echo("Logistics optimization run finished.")

@isse_cli.command()
def run_financial_sim():
    """Runs the final integrated financial Monte Carlo simulation."""
    click.echo("Running integrated financial simulation...")
    run_financial_simulation.main()
    click.echo("Financial simulation finished.")


if __name__ == '__main__':
    isse_cli()
