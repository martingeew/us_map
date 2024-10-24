import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pypalettes import load_cmap

# Read marriage data
marriage_data = pd.read_csv("https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/State_mariage_rate.csv")

# Read the shapefile
shapefile_path = "data/tl_2023_us_state.shp"
gdf = gpd.read_file(shapefile_path)

gdf.plot()

# Merge data
data = gdf.merge(marriage_data, how='inner', left_on='NAME', right_on='state')
print(len(data),len(marriage_data),len(gdf))

# Get the set of states from both DataFrames
states_in_df1 = set(gdf['NAME'])
states_in_df2 = set(marriage_data['state'])

# States in df1 but not in df2
states_not_in_intersect = states_in_df1.symmetric_difference(states_in_df2)
print(states_not_in_intersect)

# Choropleth


# Hexbin