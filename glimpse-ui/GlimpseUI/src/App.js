import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from "leaflet";
import "./SmoothWheelZoom";
const stores = [
  { name: 'Store 1', position: [51.505, -0.09] },
  { name: 'Store 2', position: [51.515, -0.1] },
];

const App = () => {

  return (
    <MapContainer
    style={{ height: "calc(100vh)", backgroundColor: "#e5e3df", width: "100%" }}
    center={[51.505, -0.09]}
    maxZoom={18}
    touchZoom={true}
    zoom={10}
    zoomControl={false}
    renderer={L.canvas()}

    smoothWheelZoom={true}
    smoothSensitivity={10}
  >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />
        
        {stores.map((store, index) => (
          <Marker key={index} position={store.position}>
            <Popup>{store.name}</Popup>
          </Marker>
        ))}
    </MapContainer>
  );
};

export default App;
