import requests
import logging
import math
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


WIND_BORNE_API_URL_CURR = "https://a.windbornesystems.com/treasure/00.json"
WIND_BORNE_API_URL_PREV = "https://a.windbornesystems.com/treasure/02.json"

class BalloonDataService:
    def __init__(self):
        self.balloon_data = self._fetch_balloon_data()
        self._cached_data = []
        self._last_update = None
        self.scheduler = BackgroundScheduler()

    def start(self):
        """Start the scheduler to update balloon data periodically"""
        self.scheduler.add_job(
            self._update_cache,
            'interval',
            minutes=60,
            id='update_balloon_data'
        )
        self.scheduler.start()
        # Initial fetch so that we can have data immediately 
        self._update_cache()
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()

    # private method 
    def _update_cache(self):
        """Update the cached balloon data"""
        try:
            logging.info("Running _update_cache() - Fetching new balloon data...")
            new_data = self._fetch_balloon_data()
            if new_data:  # Only update if we got valid data
                self._cached_data = new_data
                self._last_update = datetime.now()
                logging.info(f"Balloon data cache updated at {self._last_update}")
                # print(f"Balloon data cache updated at {self._last_update}")
        except Exception as e:
            logging.error(f"Failed to update balloon data cache: {e}")

    def _validate_and_clean_data(self, data):
        hourly_data = []
        for entry in data:
            lat, lon, alt = entry

            # Check for NaN, Inf, or -Inf and replace with default values
            if not all(map(lambda x: isinstance(x, float) and math.isfinite(x), [lat, lon, alt])):
                logging.warning(f"Invalid data found: {entry}, skipping...")
                continue  # Skip this invalid entry
            hourly_data.append({
                "latitude": lat, 
                "longitude": lon, 
                "altitude": alt,
            })

        return hourly_data
    
    # private method 
    def _fetch_balloon_data(self):
        """Fetch real-time balloon data from the Windborne API."""
        try:
            curr_response = requests.get(WIND_BORNE_API_URL_CURR)
            # curr_response.raise_for_status()  # Raise error if request fails
            curr_data = curr_response.json()  # Expecting list of [lat, lon, alt]
            
            prev_response = requests.get(WIND_BORNE_API_URL_PREV)
            # prev_response.raise_for_status()
            prev_data = prev_response.json()  # Expecting list of [lat, lon, alt]


            # Validate & clean data
            curr_formatted_data = self._validate_and_clean_data(curr_data)
            prev_formatted_data = self._validate_and_clean_data(prev_data)

            formatted_data = [curr_formatted_data, prev_formatted_data]
            return formatted_data
        except requests.RequestException as e:
            logging.error(f"Error fetching balloon data: {e}")
            return []
    
    def get_current_data(self):
        """Get the most recent balloon data"""
        if not self._cached_data:
            self._update_cache()
        return ({
            "data": self._cached_data
        })
