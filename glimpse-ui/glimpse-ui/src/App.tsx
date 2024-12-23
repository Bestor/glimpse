import * as React from 'react';
import { CssVarsProvider } from '@mui/joy/styles';
import CssBaseline from '@mui/joy/CssBaseline';
import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';

import NavBar from './components/NavBar';
import RentalCard from './components/RentalCard';
import HeaderSection from './components/HeaderSection';
import Search from './components/Search';
import Filters from './components/Filters';
import Pagination from './components/Pagination';

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from "leaflet";
import "./SmoothWheelZoom";

interface Store {
  name: string;
  position: [number, number];
}
const stores: Store[] = [
  { name: 'Store 1', position: [51.505, -0.09] },
  { name: 'Store 2', position: [51.515, -0.1] },
];

export default function RentalDashboard() {
  return (
    <CssVarsProvider disableTransitionOnChange>
      <CssBaseline />
      <NavBar />
      <Box
        component="main"
        sx={{
          height: 'calc(100vh - 55px)', // 55px is the height of the NavBar
          display: 'grid',
          gridTemplateColumns: { xs: 'auto', md: '60% 40%' },
          gridTemplateRows: 'auto 1fr auto',
        }}
      >
        <Stack
          sx={{
            backgroundColor: 'background.surface',
            px: { xs: 2, md: 4 },
            py: 2,
            borderBottom: '1px solid',
            borderColor: 'divider',
          }}
        >
          <HeaderSection />
          <Search />
        </Stack>
        <MapContainer
          style={{ height: "calc(100vh)", backgroundColor: "#e5e3df", width: "100%" }}
          center={[51.505, -0.09]}
          maxZoom={18}
          touchZoom={true}
          zoom={10}
          zoomControl={false}
          renderer={L.canvas()}
          scrollWheelZoom={false}
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
        <Stack spacing={2} sx={{ px: { xs: 2, md: 4 }, pt: 2, minHeight: 0 }}>
          <Filters />
          <Stack spacing={2} sx={{ overflow: 'auto' }}>
            <RentalCard
              title="A Stylish Apt, 5 min walk to Queen Victoria Market"
              category="Entire apartment rental in Collingwood"
              rareFind
              image="https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=400"
            />
            <RentalCard
              title="Designer NY style loft"
              category="Entire loft in central business district"
              liked
              image="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=400"
            />
            <RentalCard
              title="5 minute walk from University of Melbourne"
              category="Entire rental unit in Carlton"
              image="https://images.unsplash.com/photo-1537726235470-8504e3beef77?auto=format&fit=crop&w=400"
            />
            <RentalCard
              title="Magnificent apartment next to public transport"
              category="Entire apartment rental in Collingwood"
              image="https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=400"
            />
            <RentalCard
              title="Next to shoppng mall and public transport"
              category="Entire apartment rental in Collingwood"
              image="https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?auto=format&fit=crop&w=400"
            />
            <RentalCard
              title="Endless ocean view"
              category="A private room in a shared apartment in Docklands"
              image="https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400"
            />
            <RentalCard
              title="A Stylish Apt, 5 min walk to Queen Victoria Market"
              category="one bedroom apartment in Collingwood"
              image="https://images.unsplash.com/photo-1481437156560-3205f6a55735?auto=format&fit=crop&w=400"
            />
          </Stack>
        </Stack>
        <Pagination />
      </Box>
    </CssVarsProvider>
  );
}
