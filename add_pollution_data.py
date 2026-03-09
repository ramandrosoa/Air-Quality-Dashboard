import pandas as pd 
import numpy as np 

print("="*60)
print("GENERATING SYNTHETIC POLLUTION DATA")
print("="*60)

df = pd.read_csv('data/analysis.csv')

"""
pm 2.5 is an invisible pollution with a 2.5 µm of diameter.
"""

def generate_pollution(distance_km, parks_nearby):

    #  Base PM2.5 level for LA (random variation)
    base_pm25 = np.random.normal(25, 5) #   mean=25, std=5

    #   Distance effect: further form parks, higher pollution 
    distance_effect = min(distance_km*0.3, 5) #max effect: +5µg/m^3 at 15km, 0 at 0km

    #   Density effect: More parks nearby = lower pollution 
    density_effect = -0.8 * parks_nearby #park within 2km reduces 0.8µg/m^3

    #   Calculate pm25
    pm25 = base_pm25 + distance_effect + density_effect
    pm25 = max(5, min(45, pm25))

    #   pm10 is typically 1.6-2.0 * pm2.5
    pm10 = pm25 * np.random.uniform(1.6, 2.0)

    #   no2 correlates with pm2.5 (0.8-1.2x)
    no2 = pm25 * np.random.uniform(0.8, 1.2)

    return{
        'pm25': round(pm25, 2), 
        'pm10' : round(pm10, 2), 
        'no2' : round(no2, 2)
    }
    
print("\nGenerating pollution data based on park proximity ...")

pollution_data = []
for _, row in df.iterrows(): 
    distance = row['distance']
    park_counts = row['count_nearby_parks']

    pollution = generate_pollution(distance, park_counts)
    
    pollution_data.append(pollution)

#   Add to dataframe 
pollution_df = pd.DataFrame(pollution_data)
df = pd.concat([df, pollution_df], axis = 1)

df = df.rename(columns={
    'name' : 'station_name', 
    'location_id' : 'station_id', 
    'distance' : 'distance_to_nearest_park', 
    'count_nearby_parks' : 'parks_within_2km'
})

final_columns = ['station_name', 
                 'station_id', 
                 'city', 
                 'latitude', 
                 'longitude', 
                 'nearest_park',
                 'distance_to_nearest_park',
                 'parks_within_2km', 
                 'pm25', 
                 'pm10',
                 'no2'
                 ]

df = df[final_columns]

#   Show statistics 
print("\nPM 2.5 (µg/m^3)")
print(f"    Min: {df['pm25'].min():.2f}")
print(f"    Max: {df['pm25'].max():.2f}")
print(f"    Mean: {df['pm25'].mean():.2f}")
print(f"    Median: {df['pm25'].median():.2f}")

print("\nPM 10 (µg/m^3)")
print(f"    Min: {df['pm10'].min():.2f}")
print(f"    Max: {df['pm10'].max():.2f}")
print(f"    Mean: {df['pm10'].mean():.2f}")

print("\nNO 2 (µg/m^3)")
print(f"    Min: {df['no2'].min():.2f}")
print(f"    Max: {df['no2'].max():.2f}")
print(f"    Mean: {df['no2'].mean():.2f}")

#   Show relationship 
print("\n"+"="*60)
print("PARK PROXIMITY VS POLLUTION")
print("="*60)

#   Compare stations near VS far from parks
near_parks = df[df['distance_to_nearest_park'] < 2 ]
far_from_parks = df[df['distance_to_nearest_park'] > 8 ]

print(f"\nStations near parks (2km): {len(near_parks)}")
print(f"\nAverage pm25: {near_parks["pm25"].mean():.2f} µg/m^3")

print(f"\nStations far from parks (8km): {len(far_from_parks)}")
print(f"\nAverage pm25: {far_from_parks["pm25"].mean():.2f} µg/m^3")

if len(near_parks) > 0 and len(far_from_parks) > 0: 
    difference = far_from_parks['pm25'].mean() - near_parks['pm25'].mean()
    print(f"\nDifference : {difference:.2f} µg/m^3")
    if difference > 2 : 
        print("Stations far from parks have higher pollution")

#   Sample data
print("\nStations sorted by pollution level (ascending order):")
print(df[['station_name', 'nearest_park','distance_to_nearest_park', 'parks_within_2km', 'pm25']].sort_values('pm25').head(5))
print("\nStations sorted by pollution level (descending order):")
print(df[['station_name', 'nearest_park', 'distance_to_nearest_park', 'parks_within_2km', 'pm25']].sort_values('pm25', ascending= False).head(5))


print("\n"+"="*60)
print("SAVING TO CSV FILE")
print("="*60)
df.to_csv('data/analysis_pollution.csv')
print(f"\nData for {len(df)} stations successfully saved")

