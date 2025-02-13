from fastapi import FastAPI
from .services.balloon_data_service import BalloonDataService
from .services.wind_vector_service import WindDataService

# Initialize FastAPI app
app = FastAPI()

# Initialize BalloonDataService
balloon_service = BalloonDataService()
wind_data_service = WindDataService()

@app.get("/")
def home():
    # curr, prev
    balloon_geo_data = balloon_service._cached_data
    wind_vector_data = wind_data_service.compute_wind_vector(balloon_geo_data[0], balloon_geo_data[1])
    wind_speed_direction = wind_data_service.compute_wind_speed_direction()
    return {"message": "Drone Traffic Simulator API", "data — speed and direction": wind_speed_direction}

@app.get("/balloon_data")
def get_balloon_data():
    """Fetch cached balloon data"""
    return balloon_service._cached_data  # Serving cached data

# Start scheduler when FastAPI starts
@app.on_event("startup")
def start_scheduler():
    """Start the scheduler on app startup"""
    balloon_service.start()

# Stop scheduler when FastAPI shuts down
@app.on_event("shutdown")
def stop_scheduler():
    """Stop the scheduler on app shutdown"""
    balloon_service.stop()