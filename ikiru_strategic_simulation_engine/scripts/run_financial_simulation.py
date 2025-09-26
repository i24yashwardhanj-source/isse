# -*- coding: utf-8 -*-
"""
Script to run the integrated financial Monte Carlo simulation.
"""
from isse.models.financial_simulation import FinancialSimulator

def main():
    """
    Main function to execute the financial simulation.
    """
    # These assumptions would be loaded from a config file or derived from
    # the outputs of other models in a full pipeline.
    assumptions = {
        'd2c_rev_y0': 52_600_000,
        'b2b_rev_y0': 35_600_000,
        'd2c_growth': {'mean': 0.15, 'std': 0.05},
        'b2b_growth': {'mean': 0.20, 'std': 0.08},
        'gross_margin': 0.28,
        'op_ex_percent': 0.25,
        'discount_rate': 0.12,
    }

    simulator = FinancialSimulator(assumptions, n_simulations=10000)

    print("Running Monte Carlo financial simulation...")
    results = simulator.run_simulation()
    print("Simulation complete.")

    print("\n--- Financial Simulation Results ---")
    print(f"Mean 5-Year NPV: ₹{results['npv_mean']:,.0f}")
    print(f"Std Dev of NPV:  ₹{results['npv_std']:,.0f}")
    print("\nNPV Distribution Percentiles:")
    print(f"  5th Percentile:  ₹{results['npv_percentiles']['p5']:,.0f}")
    print(f"  50th Percentile: ₹{results['npv_percentiles']['p50']:,.0f} (Median)")
    print(f"  95th Percentile: ₹{results['npv_percentiles']['p95']:,.0f}")
    print("---------------------------------")


if __name__ == "__main__":
    main()
