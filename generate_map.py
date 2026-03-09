import folium
import pandas as pd
import json
import numpy as np
import math

#   Load data
df = pd.read_csv("data/analysis_pollution.csv")
df = df.fillna(0)

# ── single source of truth for PM2.5 classification ──
def classify_pm25(val):
    if val <= 12:  return "Good"
    if val <= 35:  return "Moderate"
    return "Unhealthy"

df["pm25_label"] = df["pm25"].apply(classify_pm25)
COLOR_MAP = {"Good": "#10B981", "Moderate": "#F59E0B", "Unhealthy": "#EF4444"}


def offset_duplicates(df, lat_col='latitude', lon_col='longitude', offset=0.0015, precision=3):
    df = df.copy()
    # round to 3 decimal places (~111m precision) to catch near-duplicates
    rounded_coords = df[[lat_col, lon_col]].round(precision).apply(tuple, axis=1)
    seen = {}

    for idx, coord in rounded_coords.items():
        if coord not in seen:
            seen[coord] = 0
        else:
            seen[coord] += 1
            angle = seen[coord] * (2 * math.pi / 6)
            df.at[idx, lat_col] = df.at[idx, lat_col] + offset * math.cos(angle)
            df.at[idx, lon_col] = df.at[idx, lon_col] + offset * math.sin(angle)

    return df

df['lat_orig'] = df['latitude']   # save real coords before shifting
df['lon_orig'] = df['longitude']
df = offset_duplicates(df)        # apply the shift

with open("data/raw/parks.json") as f:
    parks = json.load(f)

#   Center map on Los Angeles
m = folium.Map(
    location   = [34.0522, -118.2437],
    zoom_start = 11,
    tiles      = "CartoDB dark_matter"
)

# ── PARKS ──
parks_group = folium.FeatureGroup(name="🌿 Green Spaces", show=True)

for park in parks:
    folium.Marker(
        location = [park["latitude"], park["longitude"]],
        icon     = folium.DivIcon(
            html="""<div style="width:0;height:0;
                border-left:7px solid transparent;
                border-right:7px solid transparent;
                border-bottom:13px solid #4ADE80;
                filter:drop-shadow(0 0 3px rgba(74,222,128,0.6));
                "></div>""",
            icon_size=(14,13), icon_anchor=(7,13)
        ),
        tooltip = park["name"],
        popup   = folium.Popup(f"""
            <div style="font-family:monospace;font-size:12px;color:#1a1a1a;">
                <b>{park['name']}</b><br>
                <span style="color:#10B981;">🌿 Green Space</span><br>
                <small>({park['latitude']:.4f}, {park['longitude']:.4f})</small>
            </div>
        """, max_width=220)
    ).add_to(parks_group)

parks_group.add_to(m)

# ── STATIONS — ALL (main layer) ──
stations_group  = folium.FeatureGroup(name="📍 All Stations",          show=True)
good_group      = folium.FeatureGroup(name="✅ Good PM2.5 (≤12)",      show=False)
moderate_group  = folium.FeatureGroup(name="⚠️ Moderate PM2.5 (≤35)",  show=False)
unhealthy_group = folium.FeatureGroup(name="🚨 Unhealthy PM2.5 (>35)", show=False)

for _, row in df.iterrows():
    label = row["pm25_label"]
    color = COLOR_MAP[label]

    popup_html = f"""
        <div style="font-family:monospace;font-size:12px;min-width:200px;color:#1a1a1a;">
            <b style="font-size:13px;">{row['station_name']}</b><br>
            <span style="color:#666;">{row['city']}</span>
            <hr style="margin:6px 0;border-color:#eee;"/>
            <table style="width:100%;border-collapse:collapse;">
                <tr><td style="padding:3px 6px 3px 0;color:#666;">PM2.5</td>
                    <td style="font-weight:700;color:{color};">{row['pm25']:.1f} µg/m³</td></tr>
                <tr><td style="padding:3px 6px 3px 0;color:#666;">PM10</td>
                    <td style="font-weight:600;">{row['pm10']:.1f} µg/m³</td></tr>
                <tr><td style="padding:3px 6px 3px 0;color:#666;">NO₂</td>
                    <td style="font-weight:600;">{row['no2']:.1f} µg/m³</td></tr>
                <tr><td style="padding:3px 6px 3px 0;color:#666;">Nearest Park</td>
                    <td>{row['nearest_park']}</td></tr>
                <tr><td style="padding:3px 6px 3px 0;color:#666;">Distance</td>
                    <td>{row['distance_to_nearest_park']:.2f} km</td></tr>
                <tr><td style="padding:3px 6px 3px 0;color:#666;">Parks ≤2km</td>
                    <td>{int(row['parks_within_2km'])}</td></tr>
                <tr><td style="padding:3px 6px 3px 0;color:#666;">Coordinates</td>
                    <td>{row['lat_orig']:.4f}, {row['lon_orig']:.4f}</td></tr>
            </table>
            <div style="margin-top:8px;padding:4px 10px;border-radius:12px;
                background:{color}22;color:{color};font-weight:700;
                font-size:11px;display:inline-block;">{label}</div>
        </div>
    """

    # ✅ create markers directly — no nested function
    folium.CircleMarker(
        location     = [row["latitude"], row["longitude"]],
        radius       = 9,
        color        = color,
        fill         = True,
        fill_color   = color,
        fill_opacity = 0.85,
        weight       = 2,
        tooltip      = f"{row['station_name']} — {label} — PM2.5: {row['pm25']:.1f} µg/m³",
        popup        = folium.Popup(popup_html, max_width=260)
    ).add_to(stations_group)

    folium.CircleMarker(
        location     = [row["latitude"], row["longitude"]],
        radius       = 9,
        color        = color,
        fill         = True,
        fill_color   = color,
        fill_opacity = 0.85,
        weight       = 2,
        tooltip      = f"{row['station_name']} — {label} — PM2.5: {row['pm25']:.1f} µg/m³",
        popup        = folium.Popup(popup_html, max_width=260)
    ).add_to(
        good_group      if label == "Good"      else
        moderate_group  if label == "Moderate"  else
        unhealthy_group
    )

stations_group.add_to(m)
good_group.add_to(m)
moderate_group.add_to(m)
unhealthy_group.add_to(m)

# ── LEGEND ──
legend_html = """
<div style="
    position:fixed;bottom:30px;left:30px;z-index:1000;
    background:rgba(13,26,24,0.92);border:1px solid #163028;
    border-radius:10px;padding:14px 18px;
    font-family:'Courier New',monospace;font-size:11px;color:#94C5B5;
    backdrop-filter:blur(6px);
">
    <div style="font-weight:700;color:#E2F5EF;margin-bottom:10px;
        letter-spacing:0.1em;text-transform:uppercase;font-size:10px;">PM2.5 Levels</div>
    <div style="margin-bottom:6px;">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;
            background:#10B981;margin-right:8px;vertical-align:middle;"></span>
        Good <span style="color:#3D6B5E;">≤ 12 µg/m³</span>
    </div>
    <div style="margin-bottom:6px;">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;
            background:#F59E0B;margin-right:8px;vertical-align:middle;"></span>
        Moderate <span style="color:#3D6B5E;">≤ 35 µg/m³</span>
    </div>
    <div style="margin-bottom:10px;">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;
            background:#EF4444;margin-right:8px;vertical-align:middle;"></span>
        Unhealthy <span style="color:#3D6B5E;">&gt; 35 µg/m³</span>
    </div>
    <hr style="border-color:#163028;margin:8px 0;"/>
    <div style="margin-top:6px;">
        <span style="display:inline-block;width:0;height:0;
            border-left:6px solid transparent;border-right:6px solid transparent;
            border-bottom:11px solid #4ADE80;margin-right:8px;vertical-align:middle;"></span>
        Green Space
    </div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ── LAYER CONTROL ──
folium.LayerControl(position="topright", collapsed=False).add_to(m)

# ── SAVE ──
m.save("static/map.html")
print("Map saved to static/map.html")