import networkx as nx
import numpy as np
from geopy.distance import geodesic

class RouteService:
    # Logic:
    # Nodes: possible node locations
    # Edges: potential movement paths between nodes 
    # Edge weights: 
        # euclidean distance (default)
        # wind influence (reduce for tailwinds, increase for headwinds) [additional]


    def __init__(self, grid_step=0.01):
        """
        Initialize the airspace graph.
        
        Args:
            grid_step (float): Latitude/Longitude step size (e.g., 0.01 degrees).
        """
        self.graph = nx.DiGraph()  # Directed graph
        self.grid_step = grid_step  # Grid resolution

    def add_node(self, node, wind_vector):
        lat, lon = node
        """Add a node representing a location in airspace."""
        self.graph.add_node((lat, lon), wind_vector=wind_vector)

    def add_edges(self, node):
        # connects to neighboring nodes {N,S,E,W}
        pass

    def compute_weight(self, start_node, end_node, wv):
        # compute distance
        # get wind vector at sttarting node
        # compute effect of wind in direction of momvement 
        start_lat, start_lon = start_node
        end_lat, end_lon = end_node

        distance = geodesic((start_lat, start_lon), (end_lat, end_lon)).kilometers
        # wind_vector = self.graph.nodes[start_node]['wind_vector']
        wind_vector = wv

        # Calculate movement direction vector
        movement_vector = np.array([end_lon - start_lon, end_lat - start_lat])

        # wind speed
        wind_magnitude = np.linalg.norm(wind_vector)  

        # alginment
        movement_vector = movement_vector / np.linalg.norm(movement_vector) #unit vector form 

        # influence of wind (tailwind, headwind, ...)
        wind_alignment = np.dot(wind_vector, movement_vector)
        wind_effect = wind_alignment * wind_magnitude
        
        # Adjust weight based on wind (tailwind reduces weight, headwind increases it)
        adjusted_weight = distance * (1 - 0.2 * wind_effect)  # 20% wind influence
        
        return max(0.1 * distance, adjusted_weight)  # Ensure weight stays positive

    def find_best_path():
        pass
