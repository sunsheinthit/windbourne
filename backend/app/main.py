from fastapi import FastAPI
from services.manager import Manager
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from geopy.distance import geodesic

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000",],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CityCoordinates(BaseModel):
    latitude: float
    longitude: float

class PathRequest(BaseModel):
    start_city: CityCoordinates
    end_city: CityCoordinates


Services_Manager = Manager()

@app.get("/")
def home():
    # curr, prev
    # route, weight = Services_Manager.get_shortest_path()
    return {"message": "Drone Traffic Simulator API", "route — ": None,"weight — ": None}

@app.get("/balloon-data")
def get_balloon_data():
    curr, prev = Services_Manager.Balloon_Data_Service._cached_data
    return {"balloon_data": curr}

@app.get("/wind-data")
def get_wind_data(): 
    curr, prev = Services_Manager.Balloon_Data_Service._cached_data
    wind_vectors = Services_Manager.Wind_Data_Service.compute_wind_vector(curr, prev)
    wind_data = Services_Manager.Wind_Data_Service.compute_wind_speed_direction()
    return {
        "speed_direction": wind_data
    }

@app.get("/calculate-shortest-path")
def calculate_shortest_path(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
):
 # Get current balloon positions

    curr, prev = Services_Manager.Balloon_Data_Service._cached_data
    
    # Create coordinate objects
    start_coords = {"latitude": start_lat, "longitude": start_lon}
    end_coords = {"latitude": end_lat, "longitude": end_lon}
    
    # Find nearest balloons to start and end points
    start_balloon = find_nearest_balloon(start_coords, curr)
    end_balloon = find_nearest_balloon(end_coords, curr)

    start_balloon = (start_balloon['latitude'], start_balloon['longitude'])
    end_balloon = (end_balloon['latitude'], end_balloon['longitude'])

    # Calculate path between these balloons
    route, weight = Services_Manager.get_shortest_path(start_balloon, end_balloon)

    return {
        "route": route,
        "weight": weight,
        "start_balloon": start_balloon,
        "end_balloon": end_balloon
    }

def find_nearest_balloon(coords, balloons):
    """Find the balloon nearest to the given coordinates"""
    nearest = None
    min_distance = float('inf')

    for balloon in balloons:
        distance = geodesic(
            (coords['latitude'], coords['longitude']),
            (balloon['latitude'], balloon['longitude'])
        ).kilometers

        if distance < min_distance:
            min_distance = distance
            nearest = balloon

    return nearest


# Start scheduler when FastAPI starts
@app.on_event("startup")
def start_scheduler():
    """Start the scheduler on app startup"""
    Services_Manager.start_data_collection()

# Stop scheduler when FastAPI shuts down
@app.on_event("shutdown")
def stop_scheduler():
    """Stop the scheduler on app shutdown"""
    Services_Manager.stop_data_collection()