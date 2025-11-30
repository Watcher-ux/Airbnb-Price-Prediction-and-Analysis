import streamlit as st
import pandas as pd
import numpy as np
import joblib
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# ------------------
# PAGE CONFIG
# ------------------
st.set_page_config(
    page_title="Amsterdam Airbnb Price Explorer",
    layout="wide"
)

st.title("Amsterdam Airbnb Price Explorer 🏠💶")
st.markdown("Map of listings with **predicted prices**, neighbourhood filters, and geo-boundaries.")

# ------------------
# LOADERS (cached)
# ------------------
@st.cache_resource
def load_model(path: str):
    return joblib.load(path)

@st.cache_data
def load_data(listing_path: str, neigh_csv_path: str, neigh_geojson_path: str):
    df = pd.read_csv(listing_path)
    gdf = gpd.read_file(neigh_geojson_path)
    neigh_df = pd.read_csv(neigh_csv_path)
    return df, neigh_df, gdf

# ------------------
# FILE PATHS
# ------------------
MODEL_PATH = "C:/Zcommon/trainee/project_1/final_price_model.pkl"
LISTINGS_PATH = "C:/Zcommon/trainee/project_1/amster_with_preds.csv"
NEIGH_CSV_PATH = "C:/Zcommon/trainee/project_1/airbnb_/neighbourhoods_amster.csv"
NEIGH_GEOJSON_PATH = "C:/Zcommon/trainee/project_1/airbnb_/neighbourhoods_amster_geo.geojson"

# ------------------
# LOAD DATA
# ------------------
model = load_model(MODEL_PATH)
df, neigh_df, gdf = load_data(LISTINGS_PATH, NEIGH_CSV_PATH, NEIGH_GEOJSON_PATH)

# REQUIRED COLUMN CHECK
req = ["latitude", "longitude", "name", "predicted_price", "id"]
for c in req:
    if c not in df.columns:
        st.error(f"❌ Required column `{c}` missing in dataset!")
        st.stop()

# Detect neighbourhood column
neigh_col = None
for cand in ["neighbourhood_cleansed", "neighbourhood", "neighbourhood_group"]:
    if cand in df.columns:
        neigh_col = cand
        break

# ------------------
# SIDEBAR FILTERS
# ------------------
st.sidebar.header("Filters")

# Neighbourhood filter (if exists)
if neigh_col:
    neighs = sorted(df[neigh_col].dropna().unique().tolist())
    selected_neigh = st.sidebar.selectbox("Neighbourhood", options=["All"] + neighs)
else:
    selected_neigh = "All"

# Price filter
min_price = int(df["predicted_price"].min())
max_price = int(df["predicted_price"].quantile(0.99))

price_range = st.sidebar.slider(
    "Predicted price range (€)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# ------------------
# FILTER DATA
# ------------------
mask = (df["predicted_price"] >= price_range[0]) & (df["predicted_price"] <= price_range[1])

if neigh_col and selected_neigh != "All":
    mask &= (df[neigh_col] == selected_neigh)

df_filt = df[mask].copy()

if df_filt.empty:
    st.warning("⚠ No listings match your filters.")
    st.stop()

## extra addtion for rounding-off price values
df_filt["predicted_price"] = df_filt["predicted_price"].round(0)  
# ------------------
# KPI ROW
# ------------------
col1, col2, col3 = st.columns(3)
col1.metric("Listings shown", len(df_filt))
col2.metric("Avg predicted price (€)", f"{df_filt['predicted_price'].mean():.2f}")
col3.metric("Median predicted price (€)", f"{df_filt['predicted_price'].median():.2f}")

st.write("---")

# ------------------
# MAP (FOLIUM)
# ------------------
center_lat = df_filt["latitude"].mean()
center_lon = df_filt["longitude"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="CartoDB positron")

# Add neighbourhood polygons
folium.GeoJson(
    gdf,
    name="Neighbourhoods",
    style_function=lambda x: {"fillOpacity": 0, "color": "#000000", "weight": 1}
).add_to(m)

# Add listing markers
for _, row in df_filt.iterrows():
    popup_html = f"""
    <b>{row['name']}</b><br>
    🆔 ID: {row['id']}<br>
    💶 Predicted Price: €{row['predicted_price']:.2f}<br>
    {f"📍 {row[neigh_col]}" if neigh_col else ""}
    """
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=6,
        color="#ff6600",
        fill=True,
        fill_opacity=0.8,
        popup=popup_html
    ).add_to(m)

st.subheader("🗺 Map of Predicted Listings")
st_folium(m, width=1400, height=650)

# ------------------
# TABLE
# ------------------
st.subheader("📋 Filtered Listings")
display_cols = ["id", "name", "predicted_price","price", "latitude", "longitude"]
if neigh_col:
    display_cols.append(neigh_col)

st.dataframe(df_filt[display_cols].sort_values("predicted_price", ascending=False))

##END
