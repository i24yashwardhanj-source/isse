# -*- coding: utf-8 -*-
"""
Integrated Financial Simulation Module using Monte Carlo methods.

This module runs a full 5-year financial forecast, integrating outputs from
other ISSE modules and using Monte Carlo simulation to generate a probability
distribution for key financial outcomes like NPV.
"""
import numpy as np
from typing import Dict, Any

class FinancialSimulator:
    """
    Runs a Monte Carlo simulation of Ikiru's 5-year financial plan.
    """
    def __init__(self, assumptions: Dict[str, Any], n_simulations: int = 10000):
        """
        Initializes the simulator.

        Args:
            assumptions: A dictionary of financial assumptions.
            n_simulations: The number of Monte Carlo iterations to run.
        """
        self.assumptions = assumptions
        self.n_simulations = n_simulations

    def run_simulation(self) -> Dict[str, Any]:
        """
        Executes the Monte Carlo simulation.
        
        Returns:
            A dictionary containing the NPV distribution and summary statistics.
        """
        np.random.seed(42)
        
        # Extract distributions from assumptions
        d2c_growth_dist = self.assumptions['d2c_growth']
        b2b_growth_dist = self.assumptions['b2b_growth']
        
        all_npv_results = []

        for _ in range(self.n_simulations):
            # Simulate 5 years of revenue growth
            d2c_growth_path = np.random.normal(d2c_growth_dist['mean'], d2c_growth_dist['std'], 5)
            b2b_growth_path = np.random.normal(b2b_growth_dist['mean'], b2b_growth_dist['std'], 5)
            
            d2c_rev = [self.assumptions['d2c_rev_y0']]
            b2b_rev = [self.assumptions['b2b_rev_y0']]

            for i in range(5):
                d2c_rev.append(d2c_rev[-1] * (1 + d2c_growth_path[i]))
                b2b_rev.append(b2b_rev[-1] * (1 + b2b_growth_path[i]))

            total_revenue = np.array(d2c_rev) + np.array(b2b_rev)
            
            # Calculate FCF
            gross_profit = total_revenue * self.assumptions['gross_margin']
            op_ex = total_revenue * self.assumptions['op_ex_percent']
            free_cash_flow = gross_profit - op_ex
            
            # Calculate NPV of the 5 future years
            discount_rate = self.assumptions['discount_rate']
            npv = np.sum([
                fc / ((1 + discount_rate) ** (i+1)) for i, fc in enumerate(free_cash_flow[1:])
            ])
            
            all_npv_results.append(npv)

        return {
            "npv_distribution": all_npv_results,
            "npv_mean": np.mean(all_npv_results),
            "npv_std": np.std(all_npv_results),
            "npv_percentiles": {
                "p5": np.percentile(all_npv_results, 5),
                "p50": np.percentile(all_npv_results, 50),
                "p95": np.percentile(all_npv_results, 95)
            }
        }

