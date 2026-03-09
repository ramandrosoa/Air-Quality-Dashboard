import json 
import pandas as pd 

#   load data
with open('data/raw/parks.json', 'r') as f: 
    parks_data = json.load(f)

#   convert to dataframe
parks_df = pd.DataFrame(parks_data)

#   columns available 
print(f"\nColumns available:")
for col in parks_df.columns: 
    print(f"    -{col}")

#   count named VS unnamed parks 
named_count = (parks_df['name'] != 'Unnamed Park').sum()
unnamed_count = (parks_df['name'] == 'Unnamed Park').sum()

#   missing values 
print(f"\nMissing values: ")
print(parks_df[['latitude','longitude']].isnull().sum())

print(f"\nParks name:")
print(f"    Named parks: {named_count}")
print(f"    Unnamed parks: {unnamed_count}")

#   show some named parks 
print(f"\nSample named parks:")
named_parks = parks_df[parks_df['name'] != 'Unnamed Park']
for i, park in enumerate(named_parks.head(10).iterrows(), 1): 
    _, p = park
    print(f"    {i}, {p['name']}")

#   geographic range
print(f"\nGeographic coverage:")
print(f"    latitude range: {parks_df['latitude'].min():.4f} to {parks_df['latitude'].max():.4f}")
print(f"    longitude range: {parks_df['longitude'].min():.4f} to {parks_df['longitude'].max():.4f}")