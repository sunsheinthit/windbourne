import numpy as np
from geopy.distance import geodesic

class WindDataService:
    def __init__(self):
        self.wind_vectors = [] #{(u, v)} wind vector
        self.wind_speed_directions = [] # {"speed": speed, "direction": direction}

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
            lat1, lon1  = float(prev_data['latitude']), float(prev_data['longitude'])
            lat2, lon2 = float(curr_data['latitude']), float(curr_data['longitude'])

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

            self.wind_vectors.append((u, v))

        return self.wind_vectors


    def compute_wind_speed_direction(self):
        
        for u, v in self.wind_vectors:
            speed = np.sqrt(u**2 + v**2)  # Magnitude of wind vector
            direction = np.degrees(np.arctan2(u, v))  # Convert to degrees
            direction = (direction + 360) % 360  # Normalize to 0-360°

            self.wind_speed_directions.append({"speed": speed, "direction": direction})

        return self.wind_speed_directions

