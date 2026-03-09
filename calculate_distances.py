import pandas as pd
from math import radians, cos, sin, asin, sqrt
import json

def haversine_distance(lat1, lon1, lat2, lon2 ) : #(lat1, lon1): station coord, (lat2, lon2) : park coord
    """
    calculate the great circle distance between two points on Earth (specified in decimal degrees)
    returns distance in kilometers
    """
    #   convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    #   haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    d = 6357 * c

    return d

if __name__ == "__main__" : 
    print("="*60)
    print("CALCULATING DISTANCES TO NEAREST PARKS")
    print("="*60)

    #   Load data
    stations = pd.read_csv('data/raw/air_quality_stations.csv')
    with open('data/raw/parks.json', 'r') as f: 
        parks_data = json.load(f)
    parks_df = pd.DataFrame(parks_data)

    print(f"Loaded {len(stations)} stations and {len(parks_df)} parks")

    #   Test the distance function with the first park and station
    print("\nTesting distance calculation ... ")
    test_station = stations.iloc[0]
    test_park = parks_df.iloc[0]
    test_distance = haversine_distance(
        test_station['latitude'], test_station['longitude'], 
        test_park['latitude'], test_park['longitude']
    )
    print(f"    Example: {test_station['name']} to {test_park['name']}")
    print(f"    Distance: {test_distance:.2f} km")

    #   nearest park for the first 5 stations
    print("\nCalculating nearest park for first 5 stations: ")

    for idx in range(5): 
        station = stations.iloc[idx]

        min_distance = float('inf')
        nearest_park = None

        #   Check distance to every park 
        for _, park in parks_df.iterrows(): 
            distance = haversine_distance(
                station['latitude'], station['longitude'], 
                park['latitude'], park['longitude']
            )
        
            if distance < min_distance: 
                min_distance = distance
                nearest_park = park['name']

        print(f"\n  {idx+1}. {station['name']}")
        print(f"    Nearest park: {nearest_park}")
        print(f"    distance: {min_distance:.3f} km")


    print("\n" + "="*60)
    print('Distance calculation working')

