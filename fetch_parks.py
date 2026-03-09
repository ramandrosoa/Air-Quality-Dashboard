import requests
import json
import time
from config import CITY_LAT, CITY_LON

def fetch_parks_data(radius_deg=0.08):  # Smaller radius = faster
    """
    Fetch parks from OpenStreetMap - smaller area for reliability
    """
    print("Fetching parks data from OpenStreetMap...")
    print(f"Search area: {radius_deg}° around ({CITY_LAT}, {CITY_LON})")
    print("This may take 20-30 seconds...\n")
    
    url = "https://overpass-api.de/api/interpreter"
    
    lat_min = CITY_LAT - radius_deg
    lat_max = CITY_LAT + radius_deg
    lon_min = CITY_LON - radius_deg
    lon_max = CITY_LON + radius_deg
    
    # Simpler query - just parks
    query = f"""
    [out:json][timeout:45];
    (
      node["leisure"="park"]({lat_min},{lon_min},{lat_max},{lon_max});
      way["leisure"="park"]({lat_min},{lon_min},{lat_max},{lon_max});
    );
    out center 200;
    """
    
    try:
        print("Sending request (please wait)...")
        response = requests.get(url, params={'data': query}, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            elements = data.get('elements', [])
            
            print(f"✓ Successfully fetched {len(elements)} parks\n")
            
            parks = []
            for element in elements:
                if 'lat' in element and 'lon' in element:
                    lat, lon = element['lat'], element['lon']
                elif 'center' in element:
                    lat = element['center']['lat']
                    lon = element['center']['lon']
                else:
                    continue
                
                tags = element.get('tags', {})
                parks.append({
                    'id': element.get('id'),
                    'name': tags.get('name', 'Unnamed Park'),
                    'latitude': lat,
                    'longitude': lon
                })
            
            # Save
            with open('data/raw/parks.json', 'w') as f:
                json.dump(parks, f, indent=2)
            
            print(f"✓ Saved {len(parks)} parks to data/raw/parks.json")
            
            # Show samples
            print("\nSample parks:")
            named = [p for p in parks if p['name'] != 'Unnamed Park']
            for p in named[:10]:
                print(f"  - {p['name']}")
            
            print(f"\n✓ Parks data complete!")
            return parks
            
        else:
            print(f"✗ Error: {response.status_code}")
            return None
            
    except requests.Timeout:
        print("✗ Timeout. Overpass API is slow. Wait 2 minutes and try again.")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

if __name__ == "__main__":
    fetch_parks_data()