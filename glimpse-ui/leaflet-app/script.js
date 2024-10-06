// Initialize the map and set its view to a default geographical location and zoom level
// var map = L.map('map').setView([40.7128, -74.0060], 13);

initial_view_coords = [40.7128, -74.0060]

var map = L.map('map', {
    scrollWheelZoom: false, // disable original zoom function
    smoothWheelZoom: true,  // enable smooth zoom 
    smoothSensitivity: 1,   // zoom speed. default is 1
  }).setView(initial_view_coords, 13);;
// Add a tile layer to the map (OpenStreetMap tiles)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Function to add a pin to the map at a specific latitude and longitude
function addPin(lat, lon, popupText, linkUrl, linkText) {
    console.log("COORD")
    console.log(lat)
    console.log(lon)
    // const popupContent = `
    //     ${incident.popupText} <br>
    //     <a href="${incident.linkUrl}" target="_blank">${incident.linkText}</a>
    // // `;
    const popupContent = `${incident.popupText} <br><p><audio width='300' height='32' src='${incident.linkUrl}', controls='controls'><br />Your browser does not support the audio element.<br /></audio></p>`;
    L.marker([lat, lon]).addTo(map)
        .bindPopup(popupContent)
        .openPopup();
} 

var incidents = [
    {popupText: "penis", linkUrl: "https://file-examples.com/storage/fefda3519566d3360a0efb3/2017/11/file_example_MP3_700KB.mp3" ,
    linkText: "audio file", lat: 40.4233, lon: -104.7091},
    {popupText: "penis2", linkUrl: "https://www.biolifesummits.com/", linkText: "biolife", lat: 40.4300, lon: -104.7100},
    {linkText: "Bowser got peach and is driving 90mph on the freeway", lat: 40.4400, lon: -104.7200},
    {description: "Smoke detector set off", lat: 40.4600, lon: -104.6990},
    {description: "Fire reported in backyard barn", lat: 40.4200, lon: -104.7100},
    {description: "Smell of Fuel reported", lat: 40.4400, lon: -104.7300},
    {description: "Firefighters responding to down tree", lat: 40.4113, lon: -104.7091},
    {description: "fumigation in progress", lat: 40.4400, lon: -104.7900},
    {description: "Car accident involving blue ford", lat: 40.4700, lon: -104.7200},
    {description: "Plane crash at DIA", lat: 39.8563, lon: -104.6764},
];

currentIndex = 0
// Handle form submission
document.getElementById('pin-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent form from refreshing the page

    // for (const incident of incidents) {
    //     addPin(incident.lat, incident.lon, incident.description)
    //     setTimeout(3)
    // }
    if (currentIndex < incidents.length) {
        incident = incidents[currentIndex]
        currentIndex++;
        addPin(incident.lat, incident.lon, incident.popupText, incident.linkUrl, incident.linkText)

    } else {
        console.log('You have reached the end of the list.');
    }


    // Optionally, clear the form fields after submission
    document.getElementById('pin-form').reset();
});

// Define the API URL
const apiUrl = 'https://nominatim.openstreetmap.org/search?addressdetails=1&q=185+50th+Ave+Pl&format=jsonv2&limit=1';

// Make a GET request
fetch(apiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
