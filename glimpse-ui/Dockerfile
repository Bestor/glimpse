FROM cgr.dev/chainguard/node:latest-dev

USER root
COPY GlimpseUI /app
WORKDIR /app

RUN apk add curl
#RUN yarn add expo

RUN npm config set legacy-peer-deps true
#RUN npm install expo@52.0.18
RUN npm install react@rc react-dom@rc leaflet
RUN npm install react-leaflet@next
RUN npm install -D @types/leaflet
RUN npm install @mui/joy @emotion/react @emotion/styled 
RUN npm install @fontsource/inter