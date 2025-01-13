import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_custom_colormap():
    """
    Create a custom color gradient with grey in the middle.

    Returns:
        LinearSegmentedColormap: A custom colormap.
    """
    colors = [
        (0.0, "#0000D0"),  # Start with blue
        (0.5, "#D0D0D0"),  # Middle is grey
        (1.0, "#D00000")   # End with red
    ]
    return LinearSegmentedColormap.from_list("bgr_gradient", colors)

custom_cmap = create_custom_colormap()  # Initialize the colormap

def plot_lollipop(category, metrics, values, ax):
    """
    Plots a lollipop chart for a given category.

    Parameters:
        category (str): Name of the category (e.g., 'Fantasy Value').
        metrics (list): List of metric names for the category.
        values (list): List of corresponding values for the metrics.
        ax (matplotlib.axes.Axes): The subplot axis to draw on.
    """
    y_positions = range(len(metrics))  # Create y positions for the bars
    for y, (metric, value) in zip(y_positions, zip(reversed(metrics), reversed(values))):
        normalized_value = value / 100  # Normalize value to [0, 1] for colormap
        color = custom_cmap(normalized_value)  # Get color based on normalized value

        # Draw the background bar (grey line)
        ax.hlines(y=y, xmin=-5, xmax=100, linewidth=8, color='#D0D0D0', zorder=0)

        # Draw the main lollipop bar
        ax.hlines(y=y, xmin=-5, xmax=value, linewidth=20, color=color, zorder=1)

        # Draw the scatter point (lollipop head)
        ax.scatter(x=value, y=y, s=500, color=color, edgecolors='white', linewidth=1.5, zorder=3)

        # Add the value as a label inside the lollipop head
        ax.text(x=value, y=y, s=f'{round(value)}', va='center', ha='center', color='white', fontsize=9, fontweight='bold', zorder=4)

    # Style the plot
    ax.set_xlim(-5, 110)
    ax.set_ylim(-0.5, len(metrics) - 0.5)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(reversed(metrics), fontsize=8)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis='x', which='both', length=0, labelbottom=False)
    ax.tick_params(axis='y', which='both', length=0)

def calculate_figure_height(categories, bar_height=0.5):
    """
    Calculate the total height of the figure based on the number of bars.

    Parameters:
        categories (dict): Dictionary of categories and their metrics.
        bar_height (float): Height allocated per bar.

    Returns:
        float: Total figure height.
    """
    total_bars = sum(len(metrics) for metrics in categories.values())
    return total_bars * bar_height

def setup_figure_and_gridspec(categories):
    """
    Create a figure and GridSpec layout for the lollipop charts.

    Parameters:
        categories (dict): Dictionary of categories and their metrics.

    Returns:
        tuple: (figure, GridSpec object)
    """
    fig_height = calculate_figure_height(categories)
    fig = plt.figure(figsize=(4.5, fig_height))
    gs = GridSpec(nrows=len(categories), ncols=1, height_ratios=[len(categories[key]) for key in categories])
    return fig, gs

def generate_lollipop_chart(categories, values, title, subtitle):
    """
    Generate a lollipop chart for all categories.

    Parameters:
        categories (dict): Dictionary of categories and their metrics.
        values (dict): Dictionary of values corresponding to the categories.
        title (str): Main title of the chart.
        subtitle (str): Subtitle for additional player information.
    """
    fig, gs = setup_figure_and_gridspec(categories)

    for i, (category, metrics) in enumerate(categories.items()):
        ax = fig.add_subplot(gs[i])
        plot_lollipop(category, metrics, values[category], ax)
        ax.set_title(category, fontsize=11, fontweight='bold', loc='left', pad=5)

    # Add main title and subtitle
    fig.suptitle(t=title, fontweight='bold')
    fig.text(0.5, 0.9, subtitle, ha='center', fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    # Display the chart
    logging.info("Displaying the lollipop chart.")
    plt.show()
