import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pypalettes import load_cmap
import matplotlib.patches as mpatches
from drawarrow import fig_arrow, ax_arrow
from highlight_text import fig_text, ax_text
from pyfonts import load_font

# load the fonts
font = load_font(
    "https://github.com/dharmatype/Bebas-Neue/blob/master/fonts/BebasNeue(2018)ByDhamraType/ttf/BebasNeue-Regular.ttf?raw=true"
)
other_font = load_font(
    "https://github.com/bBoxType/FiraSans/blob/master/Fira_Sans_4_3/Fonts/Fira_Sans_TTF_4301/Normal/Roman/FiraSans-Light.ttf?raw=true"
)
other_bold_font = load_font(
    "https://github.com/bBoxType/FiraSans/blob/master/Fira_Sans_4_3/Fonts/Fira_Sans_TTF_4301/Normal/Roman/FiraSans-Medium.ttf?raw=true"
)
text_color = "black"


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
            # s=f"{state.upper()}: {rate:.2f}",
            s=f"{state.upper()}",
            fontsize=8,
            ha="center",
            va="center",
            fontweight="bold",
        )


def annotate_state_with_arrows(
    data,
    fig,
    state_code,
    column_name,
    tail_position,
    head_position,
    text_x,
    text_y,
    radius,
):
    """
    Annotates a state on a plot with an arrow and text label.

    Parameters:
    - data: DataFrame containing the data for states.
    - fig: Plotly or matplotlib figure object.
    - state_code: str, the two-letter code for the state to annotate (e.g., 'NJ').
    - column_name: str, the column in the data containing the value to plot.
    - tail_position: tuple, (x, y) starting position of the arrow.
    - head_position: tuple, (x, y) end position of the arrow head.
    - text_x: float, x-coordinate for text placement.
    - text_y: float, y-coordinate for text placement.
    """
    # Define arrow properties
    arrow_props = dict(width=0.5, head_width=2, head_length=4, color="black")

    # Retrieve the value to annotate
    state_value = data.loc[data["STUSPS"] == state_code, column_name].values[0]

    # Draw the arrow
    fig_arrow(
        tail_position=tail_position,
        head_position=head_position,
        radius=radius,
        **arrow_props,
    )

    # Add the text annotation
    fig_text(
        s=f"<{state_code}>: {state_value:.2f}",
        x=text_x,
        y=text_y,
        highlight_textprops=[{"font": other_bold_font}],
        color=text_color,
        fontsize=9,
        font=other_font,
        ha="center",
        va="center",
        fig=fig,
    )


def plot_with_legend(data, ax, xlim, ylim):
    """
    Plots the data on the provided axis with optional legend.

    Parameters:
    - data: GeoDataFrame to plot.
    - ax: Matplotlib axis to plot on.
    - xlim: Tuple for x-axis limits.
    - ylim: Tuple for y-axis limits.
    - show_legend: Boolean, if True displays the legend; if False, hides the legend.
    """
    # Plot data with custom color mapping
    data.plot(
        ax=ax,
        column="binned",
        color=data["binned"].map(color_mapping),
        edgecolor="white",
        linewidth=0.5,
        legend=False,  # Disable automatic legend
    )
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


def set_background_color(ax, color="#f5f5f5"):
    """
    Sets the background color of a given subplot.

    Parameters:
    - ax: Matplotlib axis object on which to set the background color.
    - color: String, color in hex format to set as the background. Default is slight off-white (#f5f5f5).
    """
    # Turn the axis back on, but this also restores labels and ticks
    ax.set_axis_on()

    # Remove the x and y axis ticks while keeping the spines
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor(color)

    # Remove the spines
    for spine in ax.spines.values():
        spine.set_visible(False)


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

# Define column for plotting
column_to_plot = "apc_20240901"

# Project the data to EPSG:5070 and calculate centroids
data_projected = data.to_crs(epsg=5070)
data_projected["centroid"] = data_projected.geometry.centroid

# Project centroids back to original CRS
data["centroid"] = data_projected["centroid"].to_crs(data.crs)

# Add a binned column based on specified ranges
data["binned"] = pd.cut(
    data[column_to_plot],
    bins=[0, 1, 2, 3, float("inf")],
    labels=["0-1%", "1-2%", "2-3%", "3+%"],
)

# Define custom colors for each bin
color_mapping = {
    "0-1%": "#05DBF2FF",
    "1-2%": "#05C7F2FF",
    "2-3%": "#05AFF2FF",
    "3+%": "#035AA6FF",
}

# Separate Alaska, Hawaii, and the contiguous U.S.
alaska = data[data["NAME"] == "Alaska"]
hawaii = data[data["NAME"] == "Hawaii"]
contiguous_us = data[(data["NAME"] != "Alaska") & (data["NAME"] != "Hawaii")]

# Set up a 2x2 grid layout with custom size ratios
new_width = 20 * 0.5
new_height = 15 * 0.5
fig, ax = plt.subplots(
    2,
    2,
    figsize=(new_width, new_height),
    dpi=300,
    gridspec_kw={"height_ratios": [4, 1], "width_ratios": [1, 1]},
)

# Plot contiguous U.S. on the main subplot (spanning both columns in the first row)
ax_main = plt.subplot2grid((2, 2), (0, 0), colspan=2, fig=fig)
plot_with_legend(contiguous_us, ax_main, xlim=(-130, -65), ylim=(24, 55))

# Alaska plot in the second row, first column
ax_alaska = plt.subplot2grid((2, 2), (1, 0), fig=fig)
plot_with_legend(alaska, ax_alaska, xlim=(-200, -100), ylim=(50, 73))

# Hawaii plot in the second row, second column
ax_hawaii = plt.subplot2grid((2, 2), (1, 1), fig=fig)
plot_with_legend(hawaii, ax_hawaii, xlim=(-162, -152), ylim=(18, 24))

# Annotate states with arrows
annotate_state_with_arrows(
    data,
    fig,
    state_code="MA",
    column_name=column_to_plot,
    tail_position=(0.853, 0.65),
    head_position=(0.815, 0.63),
    text_x=0.88,
    text_y=0.65,
    radius=0.2,
)

# Annotate states with arrows
annotate_state_with_arrows(
    data,
    fig,
    state_code="RI",
    column_name=column_to_plot,
    tail_position=(0.863, 0.6),
    head_position=(0.815, 0.62),
    text_x=0.88,
    text_y=0.6,
    radius=-0.18,
)

# Annotate states with arrows
annotate_state_with_arrows(
    data,
    fig,
    state_code="CT",
    column_name=column_to_plot,
    tail_position=(0.86, 0.57),
    head_position=(0.8, 0.62),
    text_x=0.88,
    text_y=0.57,
    radius=-0.2,
)

# Annotate states with arrows
annotate_state_with_arrows(
    data,
    fig,
    state_code="NJ",
    column_name=column_to_plot,
    tail_position=(0.86, 0.525),
    head_position=(0.775, 0.58),
    text_x=0.87,
    text_y=0.515,
    radius=0.4,
)

# Annotate states with arrows
annotate_state_with_arrows(
    data,
    fig,
    state_code="DE",
    column_name=column_to_plot,
    tail_position=(0.83, 0.50),
    head_position=(0.77, 0.565),
    text_x=0.83,
    text_y=0.49,
    radius=0.35,
)

# Annotate states with arrows
annotate_state_with_arrows(
    data,
    fig,
    state_code="MD",
    column_name=column_to_plot,
    tail_position=(0.79, 0.48),
    head_position=(0.76, 0.56),
    text_x=0.79,
    text_y=0.47,
    radius=0.3,
)

# Annotate states with arrows
annotate_state_with_arrows(
    data,
    fig,
    state_code="VT",
    column_name=column_to_plot,
    tail_position=(0.76, 0.70),
    head_position=(0.8, 0.67),
    text_x=0.74,
    text_y=0.7,
    radius=-0.2,
)

# Annotate states with arrows
annotate_state_with_arrows(
    data,
    fig,
    state_code="NH",
    column_name=column_to_plot,
    tail_position=(0.8, 0.73),
    head_position=(0.815, 0.65),
    text_x=0.78,
    text_y=0.74,
    radius=-0.1,
)

outside_state_codes = [
    "NJ",
    "DE",
    "DC",
    "MD",
    "VT",
    "NH",
    "MA",
    "CT",
    "RI",
]

# Annotate the states
annotate_states(
    contiguous_us[~contiguous_us["STUSPS"].isin(outside_state_codes)],
    ax_main,
    value_col=column_to_plot,
)
annotate_states(alaska, ax_alaska, value_col=column_to_plot)
annotate_states(hawaii, ax_hawaii, value_col=column_to_plot)

for ax in fig.axes:
    ax.set_axis_off()


set_background_color(ax_hawaii)
set_background_color(ax_alaska)


legend_handles = [
    mpatches.Patch(color=color, label=label) for label, color in color_mapping.items()
]

fig.legend(
    handles=legend_handles,
    loc="lower center",
    bbox_to_anchor=(
        0.5,
        -0.02,
    ),  # Position the legend at the bottom center of the figure
    ncol=len(color_mapping),  # Arrange items in a single row
    frameon=False,
)

# Adjust plot layout
plt.subplots_adjust(hspace=0.04)
plt.savefig("test", dpi=300, bbox_inches="tight")
plt.show()


# ToDO:
# annotate extreme values only - add a annotate function that finds outliers.
# Make font colour white for some states
# offset the position slightly for some states
# set background colour for the entire figure
# Put number undeath the state letters in brackets
# add title and sub title source and autonomousecon URL
# make all lines of code commented
