import requests
import pandas as pd
from config import OPENAQ_API_KEY, CITY_LAT, CITY_LON

def fetch_air_quality_data(radius_km=25):
    """
    Fetch air quality station locations for Los Angeles area
    """
    print("Fetching air quality stations from OpenAQ...")
    print(f"Search radius: {radius_km}km around ({CITY_LAT}, {CITY_LON})\n")
    
    locations_url = "https://api.openaq.org/v3/locations"
    headers = {'X-API-Key': OPENAQ_API_KEY}
    
    all_locations = []
    page = 1
    
    while page <= 5:  # Get up to 5 pages
        params = {
            'coordinates': f'{CITY_LAT},{CITY_LON}',
            'radius': radius_km * 1000,
            'limit': 100,
            'page': page
        }
        
        print(f"Fetching page {page}...")
        response = requests.get(locations_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Stopped at page {page}")
            break
        
        data = response.json()
        results = data.get('results', [])
        
        if not results:
            break
        
        all_locations.extend(results)
        
        # Check if more pages exist
        meta = data.get('meta', {})
        if page >= meta.get('pages', 1):
            break
            
        page += 1
    
    print(f"\n✓ Found {len(all_locations)} air quality monitoring stations\n")
    
    # Process locations
    locations_list = []
    for loc in all_locations:
        # Get latest measurement if available
        latest = loc.get('latest', {})
        
        locations_list.append({
            'location_id': loc.get('id'),
            'name': loc.get('name', 'Unknown'),
            'latitude': loc.get('coordinates', {}).get('latitude'),
            'longitude': loc.get('coordinates', {}).get('longitude'),
            'city': loc.get('city'),
            'country': loc.get('country'),
            'is_monitor': loc.get('isMonitor'),
            'latest_pm25': latest.get('pm25', {}).get('value') if 'pm25' in latest else None,
            'latest_pm10': latest.get('pm10', {}).get('value') if 'pm10' in latest else None,
            'latest_no2': latest.get('no2', {}).get('value') if 'no2' in latest else None,
            'latest_datetime': latest.get('datetime') if latest else None
        })
    
    locations_df = pd.DataFrame(locations_list)
    
    # Show summary
    print("Sample stations:")
    for i, row in locations_df.head(10).iterrows():
        pm25 = f"{row['latest_pm25']:.1f}" if pd.notna(row['latest_pm25']) else "N/A"
        print(f"  {i+1}. {row['name']} - PM2.5: {pm25}")
    
    # Save to CSV
    locations_df.to_csv('data/raw/air_quality_stations.csv', index=False)
    print(f"\n✓ Saved {len(locations_df)} stations to data/raw/air_quality_stations.csv")
    
    # Summary stats
    print("\n" + "="*60)
    print("STATIONS SUMMARY:")
    print(f"  Total stations: {len(locations_df)}")
    print(f"  Stations with PM2.5 data: {locations_df['latest_pm25'].notna().sum()}")
    print(f"  Stations with PM10 data: {locations_df['latest_pm10'].notna().sum()}")
    print(f"  Stations with NO2 data: {locations_df['latest_no2'].notna().sum()}")
    print("="*60)
    
    return locations_df

if __name__ == "__main__":
    df = fetch_air_quality_data()
    print("\n✓ Air quality station data collection complete!")
    print("We have station locations with latest measurements!")