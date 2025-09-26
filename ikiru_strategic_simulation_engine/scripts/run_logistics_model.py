# -*- coding: utf-8 -*-
"""
Script to run the logistics route optimization model.
"""
import numpy as np
from isse.models.logistics_optimization import LogisticsOptimizer

def main():
    """
    Main function to execute a sample logistics optimization problem.
    """
    # This is a sample distance matrix. In a real scenario, this would be
    # generated using a geocoding API (e.g., Google Maps) based on
    # actual customer and warehouse locations.
    # Locations: 0=Depot, 1-4=Customer Locations
    distance_matrix = [
        [0, 29, 20, 21, 16],
        [29, 0, 15, 29, 28],
        [20, 15, 0, 10, 12],
        [21, 29, 10, 0, 11],
        [16, 28, 12, 11, 0],
    ]
    num_vehicles = 2

    optimizer = LogisticsOptimizer(distance_matrix, num_vehicles)

    print("Solving Vehicle Routing Problem...")
    solution = optimizer.solve()
    print("Solver finished.")

    if "error" in solution:
        print(solution["error"])
    else:
        print("\n--- Optimal Route Plan ---")
        print(f"Total distance of all routes: {solution['total_distance']} units")
        for vehicle, route in solution['routes'].items():
            print(f"  Route for {vehicle}: {' -> '.join(map(str, route))}")
        print("--------------------------")


if __name__ == "__main__":
    main()
