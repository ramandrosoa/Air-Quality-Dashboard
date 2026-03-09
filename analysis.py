import pandas as pd
import numpy as np 
from math import radians, cos, sin, asin, sqrt
import json
from calculate_distances import haversine_distance

#   Load data
stations = pd.read_csv('data/raw/air_quality_stations.csv')
with open('data/raw/parks.json', 'r') as f: 
    parks_data = json.load(f)
parks_df = pd.DataFrame(parks_data)

#   Nearest park 
def nearest_park(df1, df2): 

    df = df1.copy()
    df['nearest_park'] = None
    df['distance'] = np.nan
    
    for idx in range(len(stations)):
        station = df1.iloc[idx]
        min_distance = float('inf')
        nearest_park = None

        for _, park in df2.iterrows() : 
            distance = haversine_distance(
                station['latitude'], station['longitude'], 
                park['latitude'], park['longitude']
            )

            if distance < min_distance: 
                min_distance = distance
                nearest_park = park['name']

        df.loc[idx, 'nearest_park'] = nearest_park
        df.loc[idx, 'distance'] = min_distance

    return df

#   Count the park nearby
def count_nearby_parks(df1, df2, radius_km = 2): 

    df = df1.copy()
    df['count_nearby_parks'] = 0

    for idx in range(len(df1)):
        station = df1.iloc[idx]
        counts = 0

        for _, park in df2.iterrows(): 
            distance = haversine_distance(
                station['latitude'], station['longitude'], 
                park['latitude'], park['longitude']
            )

            if distance < radius_km: 
                counts += 1

        df.loc[idx, 'count_nearby_parks'] = counts
    
    return df

print("="*60)
print("CALCULATING GEOSPATIAL FEATURES")
print("="*60)

print("\nStep 1: Finding nearest park for each station...")
analysis_df = nearest_park(stations, parks_df)
print(f"✓ Completed! Average distance: {analysis_df['distance'].mean():.2f} km")

print("\nStep 2: Counting parks within 2km of each station...")
analysis_df = count_nearby_parks(analysis_df, parks_df, radius_km=2)
print(f"✓ Completed! Average parks nearby: {analysis_df['count_nearby_parks'].mean():.1f}")

#   Show sample results 
print("\n"+"="*60)
print("SAMPLE RESULTS")
print("="*60)
print(analysis_df[['name', 'nearest_park', 'distance', 'count_nearby_parks']].head(10))

#   Summary statistics 
print("\n"+"="*60)
print("SUMMARY STATISTICS")
print("="*60)

print("\nDistance to nearest park:")
print(f"    Min: {analysis_df['distance'].min():.2f} km")
print(f"    Max: {analysis_df['distance'].max():.2f} km")
print(f"    Mean: {analysis_df['distance'].mean():.2f} km")
print(f"    Median: {analysis_df['distance'].median():.2f} km")

print("\nParks within 2 km:")
print(f"    Min: {analysis_df['count_nearby_parks'].min()} ")
print(f"    Max: {analysis_df['count_nearby_parks'].max()} ")
print(f"    Mean: {analysis_df['count_nearby_parks'].mean()}")

print(f"\nStations with 0 parks within 2 km: {(analysis_df['count_nearby_parks'] ==0).sum()}" )
print(f"\nStations with +5 parks within 2 km : {(analysis_df['count_nearby_parks'] >= 5).sum()}")

analysis_df.to_csv('data/analysis.csv', index = False)
print(f"✓ Results successfully saved to data/analysis.csv")
