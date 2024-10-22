import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Read marriage data
mariageData = pd.read_csv("https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/State_mariage_rate.csv")

# Read the shapefile
shapefile_path = "data/tl_2023_us_state.shp"
gdf = gpd.read_file(shapefile_path)

gdf.plot()

# Choropleth

# Hexbin