import numpy as np
from geopy.distance import geodesic

def compute_wind_vector(curr_data, prev_data):
    """
    Compute wind vector components (u, v, w) based on balloon GPS data.
    
    Args:
        curr_data (list): [[lat, lon, alt]] of current measurement
        prev_data (list): [[lat, lon, alt]] of previous measurement

    Returns:
        tuple: (u, v, w) wind vector components in m/s
    """
    wind_vectors = []

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

        wind_vectors.append((u, v, w))

    return wind_vectors
