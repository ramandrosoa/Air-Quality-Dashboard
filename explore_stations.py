import pandas as pd

stations = pd.read_csv('data/raw/air_quality_stations.csv')

#   show columns 
print(f"\nColumns available: ")
for col in stations.columns: 
    print(f"    - {col}")

#   first 5 rows
print(f"\nFirst 5 rows: ")
print(stations[['name', 'latitude', 'longitude', 'country']].head(5))

#   missing values
print(f"\nMissing values: ")
print(stations[['latitude', 'longitude']].isnull().sum())

#   geographic range
print(f"\nGeographic coverage: ")
print(f"    Latitude range: {stations['latitude'].min():.4f} to {stations['latitude'].max():.4f}")
print(f"    Longitude range: {stations['longitude'].min():.4f} to {stations['longitude'].max():.4f}")