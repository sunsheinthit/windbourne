from fastapi import FastAPI
from services.manager import Manager
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def calculate_shortest_path():
    route, weight = Services_Manager.get_shortest_path()
    return { "route": route, }


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