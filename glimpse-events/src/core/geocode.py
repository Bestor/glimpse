from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def search_address(address):
    try:
        # Initialize Nominatim API
        geolocator = Nominatim(user_agent="glimpse-events")
        print(f"searching for address: {address}")
        # Geocode the address
        location = geolocator.geocode(address)

        if location:
            print(f"Address: {location.address}")
            print(f"Latitude: {location.latitude}")
            print(f"Longitude: {location.longitude}")
            return location
        else:
            print("Address not found.")
    except Exception as e:
        print(f"Geocoding error: {e}")

if __name__ == "__main__":
    # Example address to search for
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    
    # Search for the address
    search_address("20 North Pennsylvania Street")