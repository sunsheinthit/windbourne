import { useState } from "react";
import Map from "./components/Map/Map";
import PathForm from "./components/PathForm/PathForm";
import "./BalloonRouter.css"; // Create this file

function BalloonRouter() {
  const [routeData, setRouteData] = useState(null);

  const handleRouteCalculated = (data) => {
    setRouteData(data);
  };

  return (
    <div className="balloon-router">
      <div className="form-container">
        <PathForm onRouteCalculated={handleRouteCalculated} />
      </div>
      <div className="map-container">
        <Map routeData={routeData} />
      </div>
    </div>
  );
}

export default BalloonRouter;
