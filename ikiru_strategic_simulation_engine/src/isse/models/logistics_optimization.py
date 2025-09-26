# -*- coding: utf-8 -*-
"""
Logistics Optimization Module using Google OR-Tools.

This module provides functionality to solve the Capacitated Vehicle Routing
Problem (CVRP) to find the most efficient delivery routes.
"""
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from typing import List, Dict, Any

class LogisticsOptimizer:
    """
    Solves the Vehicle Routing Problem for Ikiru's delivery fleet.
    """
    def __init__(self, distance_matrix: List[List[int]], num_vehicles: int):
        """
        Initializes the optimizer.

        Args:
            distance_matrix: A 2D list representing the distances between locations.
            num_vehicles: The number of vehicles in the fleet.
        """
        self.distance_matrix = distance_matrix
        self.num_vehicles = num_vehicles
        self.num_locations = len(distance_matrix)

    def solve(self) -> Dict[str, Any]:
        """
        Solves the routing problem and returns the optimal routes.
        
        Returns:
            A dictionary containing the total distance and the routes for each vehicle.
        """
        manager = pywrapcp.RoutingIndexManager(self.num_locations, self.num_vehicles, 0)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index: int, to_index: int) -> int:
            """Returns the distance between the two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            return self._format_solution(manager, routing, solution)
        else:
            return {"error": "No solution found."}
    
    def _format_solution(self, manager, routing, solution) -> Dict[str, Any]:
        """Formats the solver's output into a human-readable dictionary."""
        output = {"total_distance": solution.ObjectiveValue(), "routes": {}}
        for vehicle_id in range(self.num_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)
                index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index)) # Append depot at the end
            output["routes"][f"vehicle_{vehicle_id}"] = route
        return output

