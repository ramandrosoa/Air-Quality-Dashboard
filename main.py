from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import json

#   Initialize FastAPI app 
app = FastAPI(
    title       = 'Geospatial Air Quality Analysis', 
    description = 'Analysis of park proximity and air quality in Los Angeles', 
    version     = '1.0.0'
)

#   Mount static files
app.mount("/static", StaticFiles(directory="static"), name='static')


# ── single source of truth for PM2.5 classification ──
def classify_pm25(val):
    if val <= 12:  return "Good"
    if val <= 35:  return "Moderate"
    return "Unhealthy"

#   Load data 
df = pd.read_csv("data/analysis_pollution.csv")
df = df.fillna(0)
#df = df.drop_duplicates(subset = [''])
df["pm25_label"] = df["pm25"].apply(classify_pm25)

@app.get("/", response_class=HTMLResponse)
async def home(): 
    """
    Serve the main dashboard
    """
    with open("static/index.html", 'r', encoding='utf-8') as f: 
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/stats")
async def get_stats(): 
    """
    Return summary statistics as JSON
    """
    stats = {
        "total_station"              : int(len(df)), 
        "avg_distance_to_park"       : round(float(df['distance_to_nearest_park'].mean()), 2), 
        "avg_pm25"                   : round(float(df['pm25'].mean()), 2), 
        "avg_pm10"                   : round(float(df['pm10'].mean()), 2),
        "avg_no2"                    : round(float(df['no2'].mean()), 2), 
        "correlation_distance_pm25"  : round(float(df["distance_to_nearest_park"].corr(df['pm25'])), 3), 
        "stations_near_parks"        : int((df['distance_to_nearest_park'] < 1).sum()), 
        "stations_far_parks"         : int((df['distance_to_nearest_park'] > 8).sum()), 
        "stations_no_parks_nearby"   : int((df['parks_within_2km'] == 0).sum())
    }
    return JSONResponse(content=stats)

@app.get("/api/stations")
async def get_stations():
    """
    Return all stations data as JSON
    """
    stations_data = df.to_dict(orient='records')
    return JSONResponse(content=stations_data)

@app.get("/api/stations/{station_id}")
async def get_station(station_id: int):
    """
    Return a single station by ID
    """
    station = df[df['station_id'] == station_id]
    if len(station) == 0:
        return JSONResponse(content={"error": "Station not found"}, status_code=404)
    return JSONResponse(content=station.to_dict(orient='records')[0])

@app.get("/api/parks")
async def get_parks(): 
    """
    Return parks GeoJSON data
    """
    with open('data/raw/parks.json', 'r') as f: 
        parks_data = json.load(f)
    return JSONResponse(content=parks_data)

@app.get("/api/comparison")
async def get_comparison(): 
    """
    Return comparison between far and near stations
    """
    near_stations = df[df["distance_to_nearest_park"] < 2]
    far_stations  = df[df["distance_to_nearest_park"] > 8]

    comparison = {
        "near_parks" : {
            'count'        : int(len(near_stations)), 
            'avg_pm25'     : round(float(near_stations['pm25'].mean()), 2),
            'avg_distance' : round(float(near_stations['distance_to_nearest_park'].mean()), 2)
        }, 
        "far_parks" : {
            'count'        : int(len(far_stations)), 
            'avg_pm25'     : round(float(far_stations['pm25'].mean()), 2),
            'avg_distance' : round(float(far_stations['distance_to_nearest_park'].mean()), 2)
        }, 
        "difference_pm25" : round(float(far_stations['pm25'].mean()) - float(near_stations['pm25'].mean()), 2)
    }
    return JSONResponse(content=comparison)

@app.get("/health") 
async def health_check():
    return {"status"  : "healthy", 
            "message" : "API is running"}

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
