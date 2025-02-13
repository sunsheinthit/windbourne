from fastapi import FastAPI
from .services.manager import Manager

# Initialize FastAPI app
app = FastAPI()

Services_Manager = Manager()

@app.get("/")
def home():
    # curr, prev
    route, weight = Services_Manager.get_shortest_path()
    return {"message": "Drone Traffic Simulator API", "route — ": route,"weight — ": weight}

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