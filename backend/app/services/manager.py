from .balloon_data_service import BalloonDataService
from .wind_vector_service import WindDataService
from .route_service import RouteService

class Manager:
    def __init__(self):
        self.Balloon_Data_Service = BalloonDataService()
        self.Wind_Data_Service = WindDataService()
        self.Route_service = RouteService()

    def start_data_collection(self):
        # start the data collection
        self.Balloon_Data_Service.start()

    def stop_data_collection(self):
        self.Balloon_Data_Service.stop()
    
    def get_shortest_path(self, start_balloon, end_balloon):
        # get the balloon geolocation data 
        curr, prev = self.Balloon_Data_Service._cached_data

        # get wind vectors
        wind_vectors = self.Wind_Data_Service.compute_wind_vector(curr, prev)
        self.Route_service.populate_graph(curr, wind_vectors)

        route, weight = self.Route_service.find_best_path(start_balloon, end_balloon)

        return route, weight