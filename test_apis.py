import requests
from config import OPENWEATHER_API_KEY, OPENAQ_API_KEY, CITY_LAT, CITY_LON

print("Testing API connections...\n")

# Test 1: OpenAQ (Air Quality) - v3 requires API key
print("1. Testing OpenAQ API v3...")
try:
    url = "https://api.openaq.org/v3/locations"
    headers = {'X-API-Key': OPENAQ_API_KEY}
    params = {
        'coordinates': f'{CITY_LAT},{CITY_LON}',
        'radius': 25000,  # 25km radius
        'limit': 5
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        print(f"   ✓ OpenAQ working! Found {len(results)} air quality stations")
    else:
        print(f"   ✗ Error: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: OpenWeather API, just in case openAQ and openStreetMap don't work
print("\n2. Testing OpenWeather API...")
try:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': CITY_LAT,
        'lon': CITY_LON,
        'appid': OPENWEATHER_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        temp_celsius = data['main']['temp'] - 273.15
        print(f"   ✓ OpenWeather working! Current temp: {temp_celsius:.1f}°C")
    else:
        print(f"   ✗ Error: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Overpass API (OpenStreetMap) - No key needed
print("\n3. Testing Overpass API (OpenStreetMap)...")
try:
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["leisure"="park"]({CITY_LAT-0.1},{CITY_LON-0.1},{CITY_LAT+0.1},{CITY_LON+0.1});
      way["leisure"="park"]({CITY_LAT-0.1},{CITY_LON-0.1},{CITY_LAT+0.1},{CITY_LON+0.1});
    );
    out center;
    """
    response = requests.get(url, params={'data': query})
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Overpass working! Found {len(data.get('elements', []))} parks")
    else:
        print(f"   ✗ Error: {response.status_code}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*50)
print("API testing complete!")