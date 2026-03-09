import requests
from config import CITY_LAT, CITY_LON
import time

print("Testing Overpass API with simpler query...\n")

url = "https://overpass-api.de/api/interpreter"

# Simpler, smaller query
query = f"""
[out:json][timeout:25];
(
  node["leisure"="park"]({CITY_LAT-0.05},{CITY_LON-0.05},{CITY_LAT+0.05},{CITY_LON+0.05});
  way["leisure"="park"]({CITY_LAT-0.05},{CITY_LON-0.05},{CITY_LAT+0.05},{CITY_LON+0.05});
);
out center 10;
"""

try:
    print("Sending request (this may take 10-15 seconds)...")
    response = requests.get(url, params={'data': query}, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        elements = data.get('elements', [])
        print(f"✓ Success! Found {len(elements)} parks")
        
        # Show a few examples
        if elements:
            print("\nSample parks found:")
            for i, park in enumerate(elements[:3]):
                name = park.get('tags', {}).get('name', 'Unnamed park')
                print(f"  {i+1}. {name}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except requests.Timeout:
    print("✗ Request timed out. The Overpass API is slow right now.")
    print("   Don't worry - we can try again later or use an alternative!")
    
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*50)
print("Note: Overpass can be slow. If it keeps failing,")
print("we can use an alternative approach for green spaces.")