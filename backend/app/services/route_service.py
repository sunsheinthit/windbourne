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

    def find_best_path(self, start_point, end_point):
        """
        Find the optimal path between start and end points using Dijkstra's algorithm.
        
        Args:
            start_point (tuple): Starting coordinates (lat, lon) [WILL BE CLOSEST BALLOON]
            end_point (tuple): Ending coordinates (lat, lon) [WILL BE CLOSEST BALLOON]
        Returns:
            tuple: (path, total_distance) where path is a list of coordinates and 
                  total_distance is the cumulative weighted distance
        """
        try:
            # Find the shortest path using Dijkstra's algorithm
            path = nx.shortest_path(
                self.graph, 
                source=start_point, 
                target=end_point, 
                weight='weight'
            )
            
            # Calculate total distance (sum of edge weights along the path)
            total_distance = nx.shortest_path_length(
                self.graph, 
                source=start_point, 
                target=end_point, 
                weight='weight'
            )
            
            return path, total_distance
            
        except nx.NetworkXNoPath:
            print("NO PATH EXISTS")
            return None, None  # Return None if no path exists

    def populate_graph(self, node_list, wind_vector_list):
        """Populate Graph Nodes and Edges"""
        # nodes
        for node, wind_vector in zip(node_list, wind_vector_list):
            self._add_node(node, wind_vector)
        print(f"Added {len(self.graph.nodes)} nodes to graph")
        print(self.graph.nodes)
        # edges
        for node in node_list:
            self._add_edges(node)
        print(f"Added {len(self.graph.edges)} edges to graph")


    def _add_node(self, node, wind_vector):
        """Add a node representing a location in airspace."""
        lat, lon, = float(node['latitude']), float(node['longitude'])
        self.graph.add_node((lat, lon), wind_vector=wind_vector)

    def _add_edges(self, node):
        """
        Add edges from the given node to its neighboring nodes in cardinal directions.
        
        Args:
            node (tuple): Current node coordinates (lat, lon)
        """
        lat, lon, = float(node['latitude']), float(node['longitude'])
        # Define neighboring positions using grid_step
        neighbors = [
            (lat + self.grid_step, lon),    # North
            (lat - self.grid_step, lon),    # South
            (lat, lon + self.grid_step),    # East
            (lat, lon - self.grid_step)     # West
        ]
        
        # Add edges to existing neighbors
        for neighbor in neighbors:
            if neighbor in self.graph:
                # Add directed edge from current node to neighbor
                weight = self._compute_weight(node, neighbor)
                self.graph.add_edge(node, neighbor, weight=weight)
                
                # Add directed edge from neighbor to current node
                reverse_weight = self._compute_weight(neighbor, node)
                self.graph.add_edge(neighbor, node, weight=reverse_weight)

    def _compute_weight(self, start_node, end_node):
        # compute distance
        # get wind vector at sttarting node
        # compute effect of wind in direction of momvement 
        start_lat, start_lon = start_node
        end_lat, end_lon = end_node

        distance = geodesic((start_lat, start_lon), (end_lat, end_lon)).kilometers
        wind_vector = self.graph.nodes[(start_lat, start_lon)]['wind_vector'] # wind vector is needed here

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
