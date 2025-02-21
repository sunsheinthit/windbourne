import { useEffect, useState, useRef } from "react";
import L from "leaflet";
import { balloon_service } from "../../services/api";
import PathForm from "../Controls/PathForm";

function Map() {
  const mapRef = useRef(null); // ref is used so it is initialized only once
  const mapContainerRef = useRef(null);
  const [balloonData, setBalloonData] = useState(null);
  const [windData, setWindData] = useState(null);
  // const [pathData, setPathData] = useState(null);

  const fetchData = async () => {
    const balloon = await balloon_service.getBalloonData();
    console.log("Raw balloon response:", balloon);

    const wind = await balloon_service.getWindData();
    console.log("Raw wind response:", wind);

    // const path = await balloon_service.calculatePath();

    setBalloonData(balloon);
    setWindData(wind);
    // setPathData(path);
  };

  useEffect(() => {
    if (mapContainerRef && !mapRef.current) {
      mapRef.current = L.map(mapContainerRef.current).setView(
        [37.7749, -122.4194],
        4
      ); // Starting at San Francisco
      //   // Add OpenStreetMap tile layer
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© OpenStreetMap contributors",
      }).addTo(mapRef.current);
    }

    fetchData();

    // Cleanup function to remove map when component unmounts
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (balloonData && windData && mapRef.current) {
      console.log("rendering data");
      // Clear existing markers
      mapRef.current.eachLayer((layer) => {
        if (layer instanceof L.Marker) {
          layer.remove();
        }
      });

      // Add markers for balloon data
      balloonData.balloon_data.forEach((balloon, index) => {
        if (balloon.latitude && balloon.longitude) {
          L.marker([balloon.latitude, balloon.longitude])
            .addTo(mapRef.current)
            .bindPopup(
              `Balloon ${index}: ${balloon.latitude}, ${balloon.longitude}`
            );
        }
      });

      // Add wind vectors
      windData.speed_direction.forEach((speedDir, index) => {
        if (index < balloonData.balloon_data.length) {
          const balloon = balloonData.balloon_data[index];
          if (balloon && speedDir) {
            // Create an arrow for the wind vector
            const arrowLength = 0.5; // Scale the arrow length
            const directionRad = (speedDir.direction * Math.PI) / 180; // Convert to radians
            const startPoint = [balloon.latitude, balloon.longitude];
            const endPoint = [
              balloon.latitude + Math.cos(directionRad) * arrowLength,
              balloon.longitude + Math.sin(directionRad) * arrowLength,
            ];

            // Draw arrow
            L.polyline([startPoint, endPoint], {
              color: "red",
              weight: 5,
            })
              .addTo(mapRef.current)
              .bindPopup(
                `Wind Speed: ${speedDir.speed.toFixed(
                  2
                )} m/s<br>Direction: ${speedDir.direction.toFixed(2)}°`
              );

            // Add arrow head (simple triangle)
            const arrowHead = L.polygon(
              [
                endPoint,
                [endPoint[0] - 0.001, endPoint[1] - 0.001],
                [endPoint[0] - 0.001, endPoint[1] + 0.001],
              ],
              {
                color: "red",
                fillColor: "red",
                fillOpacity: 1,
                weight: 1,
              }
            ).addTo(mapRef.current);
          }
        }
      });
    }
  }, [balloonData, windData]);

  return (
    <div className="MapContainer">
      {/* <PathForm /> */}
      <div ref={mapContainerRef} style={{ height: "100%", width: "100%" }} />
    </div>
  );
}

export default Map;
