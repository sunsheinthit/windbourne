import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export const balloon_service = {
  // Get wind data for the map
  getWindData: async () => {
    const response = await axios.get(`${API_BASE_URL}/wind-data`);
    return response.data;
  },

  // get balloon data
  getBalloonData: async () => {
    const response = await axios.get(`${API_BASE_URL}/balloon-data`);
    return response.data;
  },

  // Calculate path between two points
  calculatePath: async (start, end) => {
    const response = await axios.post(
      `${API_BASE_URL}/calculate-shortest-path`,
      {
        start_point: start,
        end_point: end,
      }
    );
    return response.data;
  },
};
