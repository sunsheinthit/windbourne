import numpy as np
from geopy.distance import geodesic

class WindDataService:
    def __init__(self):
        self.wind_vectors = []
        self.wind_speed_directions = []

    def compute_wind_vector(self, curr_data, prev_data):
        """
        Compute wind vector components (u, v, w) based on balloon GPS data.
        
        Args:
            curr_data (list): [[lat, lon, alt]] of current measurement
            prev_data (list): [[lat, lon, alt]] of previous measurement

        Returns:
            tuple: (u, v, w) wind vector components in m/s
        """

        for prev_data, curr_data in zip(curr_data, prev_data):
            lat1, lon1, alt1 = float(prev_data['latitude']), float(prev_data['longitude']), float(prev_data['altitude'])
            lat2, lon2, alt2 = float(curr_data['latitude']), float(curr_data['longitude']), float(curr_data['altitude'])

            print("HELLO WOLRD",lat1,lat1)
            print(type(lat1),type(lat1))
            # Time difference of 1 hour
            dt = 3600 # seconds

            # Compute horizontal distance using geodesic
            d_horiz = geodesic((lat1, lon1), (lat2, lon2)).meters
            
            # Compute azimuth angle (direction of movement)
            delta_lon = lon2 - lon1
            delta_lat = lat2 - lat1
            azimuth = np.arctan2(delta_lon, delta_lat)  # Angle in radians

            # Compute wind components (u, v)
            u = (d_horiz / dt) * np.sin(azimuth)  # East-West component
            v = (d_horiz / dt) * np.cos(azimuth)  # North-South component
            w = (alt2 - alt1) / dt  # Vertical component

            self.wind_vectors.append((u, v, w))

        return self.wind_vectors


    def compute_wind_speed_direction(self):
        
        for u, v, w in self.wind_vectors:
            speed = np.sqrt(u**2 + v**2)  # Magnitude of wind vector
            direction = np.degrees(np.arctan2(u, v))  # Convert to degrees
            direction = (direction + 360) % 360  # Normalize to 0-360°

            self.wind_speed_directions.append({"speed": speed, "direction": direction, "vertical_speed": w})

        return self.wind_speed_directions

