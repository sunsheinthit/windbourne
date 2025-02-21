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
        self.epsilon = 0.01 #error tolerance

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
            lat, lon, = float(node['latitude']), float(node['longitude'])
            self._add_node((lat, lon), wind_vector)

        print(f"Added {len(self.graph.nodes)} nodes to graph")
        for node, data in self.graph.nodes(data=True):
            # Open file in write mode
            with open('node_data.txt', 'w') as f:
                for node, data in self.graph.nodes(data=True):
                    f.write(f"Node: {node}, Data: {data}\n")
                    print(f"Node: {node}, Data: {data}")  # Keep the print statement if you still want console output


        # edges
        for node in node_list:
            lat, lon, = float(node['latitude']), float(node['longitude'])
            self._add_edges((lat, lon))

        print(f"Added {len(self.graph.edges)} edges to graph")



    def _add_node(self, node, wind_vector):
        """Add a node representing a location in airspace."""
        self.graph.add_node(node, wind_vector=wind_vector)

    def _add_edges(self, node):
        """Add edges from the given node to its neighboring nodes."""
        current_node = node[0], node[1]
        print(f"\nTrying to add edges for node: {current_node}")
        
        edges_added = 0
        # Connect to all nodes within reasonable distance
        for other_node in self.graph.nodes():
            if other_node == current_node:
                continue
                
            # Calculate Manhattan distance (since we rounded to integers)
            lat_diff = abs(current_node[0] - other_node[0])
            lon_diff = abs(current_node[1] - other_node[1])
            manhattan_dist = lat_diff + lon_diff
            
            print(f"Checking potential neighbor: {other_node}")
            print(f"Manhattan distance: {manhattan_dist}")
            
            # Connect if within 3 grid units (adjust this value as needed)
            if manhattan_dist <= 25:
                print(f"Adding edge to neighbor: {other_node}")
                # Add directed edge from current node to neighbor
                weight = self._compute_weight(current_node, other_node)
                self.graph.add_edge(current_node, other_node, weight=weight)
                
                # Add directed edge from neighbor to current node
                reverse_weight = self._compute_weight(other_node, current_node)
                self.graph.add_edge(other_node, current_node, weight=reverse_weight)
                
                edges_added += 2
        
        print(f"Total edges added for node {current_node}: {edges_added}")


    def _compute_weight(self, start_node, end_node):
        # compute distance
        # get wind vector at sttarting node
        # compute effect of wind in direction of momvement 
        start_lat, start_lon = start_node
        end_lat, end_lon = end_node

        distance = geodesic((start_lat, start_lon), (end_lat, end_lon)).kilometers

        wind_vector = self.graph.nodes[start_node]['wind_vector'] # wind vector is needed here

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
        adjusted_weight = distance * (1 - 0.05 * wind_effect)  # 20% wind influence
        
        return max(0.1 * distance, adjusted_weight)  # Ensure weight stays positive
