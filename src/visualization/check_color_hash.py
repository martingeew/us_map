import matplotlib.pyplot as plt

# # List of color hash codes

hash_codes = [
    "#FFB07AFF",  # Orange
    "#66F0FAFF",  # Light blue
    "#66CCFFFF",  # Slightly darker blue
    "#33B2FFFF",  # Darker blue
    "#035AA6FF",  # Darkest blue
]


# Create a figure to display the colors
fig, ax = plt.subplots(figsize=(8, 2))

# Iterate over the hash codes to display each color as a horizontal bar
for i, color in enumerate(hash_codes):
    ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
    ax.text(i + 0.5, -0.3, color, ha="center", va="center", fontsize=10)

# Set the x and y limits
ax.set_xlim(0, len(hash_codes))
ax.set_ylim(-1, 1)

# Remove axes
ax.axis("off")

# Show the figure
plt.show()
