import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pypalettes import load_cmap


# Function to annotate states
def annotate_states(geo_df, ax, value_col):
    states_to_annotate = list(geo_df["STUSPS"].unique())
    for state in states_to_annotate:
        centroid = geo_df.loc[geo_df["STUSPS"] == state, "centroid"].values[0]
        x, y = centroid.coords[0]
        rate = geo_df.loc[geo_df["STUSPS"] == state, value_col].values[0]
        ax.text(
            x=x,
            y=y,
            s=f"{state.upper()}: {rate:.2f}",
            fontsize=9,
            ha="center",
            va="center",
            fontweight="bold",
        )


def turn_on_spines(ax, spine_width=1):
    """
    Turn on the spines for a given axes object after the axis has been turned off.
    Optionally, set the width of the spines.

    Parameters:
    - ax: The axes object for which to turn on the spines.
    - spine_width: The width of the spines (default is 1).
    """
    # Turn the axis back on, but this also restores labels and ticks
    ax.set_axis_on()

    # Remove the x and y axis ticks while keeping the spines
    ax.set_xticks([])
    ax.set_yticks([])

    # Turn on the spines for all sides
    ax.spines["top"].set_visible(True)
    ax.spines["bottom"].set_visible(True)
    ax.spines["left"].set_visible(True)
    ax.spines["right"].set_visible(True)

    # Set the border (spine) width
    for spine in ax.spines.values():
        spine.set_linewidth(spine_width)


# Read marriage data
marriage_data = pd.read_csv(
    "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/State_mariage_rate.csv"
)

employment_data = pd.read_csv(
    "data\employment_state_apc_20240901_pivot.csv", index_col=0
)

# Read the shapefile
shapefile_path = "data/tl_2023_us_state.shp"
gdf = gpd.read_file(shapefile_path)

gdf.plot()

# Merge data
data = gdf.merge(employment_data, how="inner", left_on="STUSPS", right_on="State")
print(len(data), len(employment_data), len(gdf))

# Get the set of states from both DataFrames
states_in_df1 = set(gdf["STUSPS"])
states_in_df2 = set(employment_data["State"])

# States in df1 but not in df2
states_not_in_intersect = states_in_df1.symmetric_difference(states_in_df2)
print(states_not_in_intersect)

# Choropleth

# Load colormap
cmap = load_cmap("Bmsurface")

# Project the data to EPSG:5070
data_projected = data.to_crs(epsg=5070)
data_projected["centroid"] = data_projected.geometry.centroid

# Project the centroids back to the original CRS for correct positioning in the plot
data["centroid"] = data_projected["centroid"].to_crs(data.crs)

# Separate Alaska, Hawaii, and the contiguous U.S.
alaska = data[data["NAME"] == "Alaska"]
hawaii = data[data["NAME"] == "Hawaii"]
contiguous_us = data[(data["NAME"] != "Alaska") & (data["NAME"] != "Hawaii")]

# Set up a 2-row, 2-column grid with the main US plot spanning the entire top row,
# and Alaska and Hawaii in the second row as 2 separate columns
new_width = 20 * 0.5
new_height = 15 * 0.5
fig, ax = plt.subplots(
    2,
    2,
    figsize=(new_width, new_height),
    dpi=300,
    gridspec_kw={"height_ratios": [4, 1], "width_ratios": [1, 1]},
)

# Create the main US plot on the first row spanning both columns
ax_main = plt.subplot2grid((2, 2), (0, 0), colspan=2, fig=fig)

column_to_plot = "apc_20240901"

# Plot the contiguous U.S. on the main subplot
contiguous_us.plot(
    ax=ax_main, column=column_to_plot, cmap=cmap, edgecolor="black", linewidth=0.5
)

# Set axis properties for main plot
ax_main.set_xlim(-130, -65)
ax_main.set_ylim(24, 55)

# Alaska plot in the second row, first column
ax_alaska = plt.subplot2grid((2, 2), (1, 0), fig=fig)

# Plot Alaska in the subplot
alaska.plot(
    ax=ax_alaska, column=column_to_plot, cmap=cmap, edgecolor="black", linewidth=0.5
)
ax_alaska.set_xlim(-200, -100)
ax_alaska.set_ylim(50, 73)

# Hawaii plot in the second row, second column
ax_hawaii = plt.subplot2grid((2, 2), (1, 1), fig=fig)

# Plot Hawaii in the subplot
hawaii.plot(
    ax=ax_hawaii, column=column_to_plot, cmap=cmap, edgecolor="black", linewidth=0.5
)
ax_hawaii.set_xlim(-162, -152)
ax_hawaii.set_ylim(18, 24)

# Annotate the states
annotate_states(contiguous_us, ax_main, value_col=column_to_plot)
annotate_states(alaska, ax_alaska, value_col=column_to_plot)
annotate_states(hawaii, ax_hawaii, value_col=column_to_plot)

for ax in fig.axes:
    ax.set_axis_off()

turn_on_spines(ax_hawaii, spine_width=1)
turn_on_spines(ax_alaska, spine_width=1)

# Tight layout to ensure subplots fit well within the figure
# plt.tight_layout()
plt.subplots_adjust(hspace=0.05)
plt.savefig("test", dpi=300, bbox_inches="tight")
plt.show()


# ToDO:
# annotate extreme values only - add a annotate function that finds outliers.
# Add title for Hawaii and Alaska inside plot
# add cmap legend
# add title and sub title
# add source
# make all lines of code commented
# How to add multiple choropleth maps to show different years.

