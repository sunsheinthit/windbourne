Hello! This is my application to the WindBorne Systems SWE internship summer for the summer of 2025. 

The problem I wanted to tackle was how we can better utilize wind energy, starting with creating more efficient routes for planes by using tailwinds and avoiding headwinds. This tool not only enhances drone and aircraft efficiency but can also be applied to other sectors.

The project leveraged WindBorne's API by tracking balloons' positions and computing the wind vectors given their displacement averaged over an hour. The core functionality involves a pathfinding algorithm that optimizes flight routes based on distance and wind conditions. I utilized NetworkX, which is an API, to represent balloons as nodes, connect them via edges, and assign weights based on distance and wind influence. I then ran Dijkstra's algorithm to determine the most efficient route between two given cities. For visualization, I used Leaflet API to create an interactive map displaying the balloons, wind vectors, and the optimized flight path.

I hosted the frontend on Netlify and the backend on Render. 
