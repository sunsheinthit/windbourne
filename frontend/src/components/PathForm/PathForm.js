import { useState } from "react";
import axios from "axios";
import { balloon_service } from "../../services/api";
import "./PathForm.css";

function PathForm({ onRouteCalculated }) {
  const [startCity, setStartCity] = useState("");
  const [endCity, setEndCity] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Function to convert city to coordinates using OpenStreetMap Nominatim API
  const getCityCoordinates = async (city) => {
    try {
      const response = await axios.get(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
          city
        )}`
      );
      if (response.data && response.data.length > 0) {
        return {
          latitude: parseFloat(response.data[0].lat),
          longitude: parseFloat(response.data[0].lon),
        };
      }
      throw new Error(`Could not find coordinates for ${city}`);
    } catch (error) {
      throw new Error(
        `Error getting coordinates for ${city}: ${error.message}`
      );
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Get coordinates for both cities
      const startCoords = await getCityCoordinates(startCity);
      const endCoords = await getCityCoordinates(endCity);

      console.log("Sending coordinates:", { startCoords, endCoords });

      // Call backend to find nearest balloons and calculate path
      const response = await balloon_service.calculateShortestPath(
        {
          latitude: Math.round(startCoords.latitude * 1000000) / 1000000,
          longitude: Math.round(startCoords.longitude * 1000000) / 1000000,
        },
        {
          latitude: Math.round(endCoords.latitude * 1000000) / 1000000,
          longitude: Math.round(endCoords.longitude * 1000000) / 1000000,
        }
      );
      const routeCoords = response.route.map((point) =>
        Array.isArray(point) ? point : [point.latitude, point.longitude]
      );

      onRouteCalculated(routeCoords);
      setSuccess(true);
      console.log(routeCoords);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pathForm">
      <h2 className="formTitle">Route Calculator</h2>
      <p className="formDescription">
        Enter your start and destination cities to calculate the optimal balloon
        route.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="inputGroup">
          <label htmlFor="startCity">Start City</label>
          <input
            id="startCity"
            type="text"
            value={startCity}
            onChange={(e) => setStartCity(e.target.value)}
            placeholder="e.g., New York"
            disabled={loading}
          />
        </div>

        <div className="inputGroup">
          <label htmlFor="endCity">Destination City</label>
          <input
            id="endCity"
            type="text"
            value={endCity}
            onChange={(e) => setEndCity(e.target.value)}
            placeholder="e.g., Los Angeles"
            disabled={loading}
          />
        </div>

        <button type="submit" disabled={loading || !startCity || !endCity}>
          {loading ? (
            <>
              <span className="loadingSpinner"></span>
              Calculating...
            </>
          ) : (
            "Calculate Route"
          )}
        </button>
      </form>
      {success && <div className="success">ROUTE FOUND</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default PathForm;
