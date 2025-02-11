from fastapi import FastAPI
from .services.balloon_data_service import BalloonDataService

# Initialize FastAPI app
app = FastAPI()

# Initialize BalloonDataService
balloon_service = BalloonDataService()

@app.get("/")
def home():
    return {"message": "Drone Traffic Simulator API", "data": balloon_service._cached_data}

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