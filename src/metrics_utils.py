import pandas as pd
from scipy.stats import percentileofscore

def format_height(inches):
    """
    Convert height in inches to a string in feet and inches (e.g., 6'4").

    Args:
        inches (float or int): Height in inches.

    Returns:
        str: Height formatted as feet and inches.
    """
    feet = int(inches // 12)  # Get the number of whole feet
    remaining_inches = int(inches % 12)  # Get the remaining inches
    return f"{feet}'{remaining_inches}\""


def calculate_percentile_from_qualifying(data, stat, qualifying_stat, min_attempts):
    """
    Calculate percentiles for a stat using only qualifying players for the distribution.

    Args:
        data (pd.DataFrame): DataFrame containing player stats.
        stat (str): Column name for the stat to calculate percentiles.
        qualifying_stat (str): Column name used to determine qualification.
        min_attempts (int): Minimum attempts required to qualify.

    Returns:
        pd.Series: Percentile values for all players based on qualifying players' distribution.
    """
    # Filter qualifying players
    qualifying_players = data[data[qualifying_stat] >= min_attempts][stat].dropna()

    if qualifying_players.empty:
        raise ValueError(f"No qualifying players found for {stat} with {qualifying_stat} >= {min_attempts}.")

    # Calculate percentiles for all players based on the qualifying distribution
    return data[stat].apply(lambda x: percentileofscore(qualifying_players, x, kind='rank'))

def calculate_passing_fantasy_points(data):
    """
    Calculate completion percentage for all players in the dataset.

    Args:
        data (pd.DataFrame): DataFrame containing 'completions' and 'attempts' columns.

    Returns:
        pd.Series: A Series containing completion percentage for each player.
    """
    if 'rushing_yards' not in data.columns or 'rushing_tds' not in data.columns:
        raise ValueError("The DataFrame must contain 'completions' and 'attempts' columns.")
    
    return (data['passing_yards']*0.1 + data['passing_tds']*6 + data['passing_2pt_conversions']*2 + data['interceptions']*(-2))

def calculate_rushing_fantasy_points(data):
    """
    Calculate completion percentage for all players in the dataset.

    Args:
        data (pd.DataFrame): DataFrame containing 'completions' and 'attempts' columns.

    Returns:
        pd.Series: A Series containing completion percentage for each player.
    """
    if 'rushing_yards' not in data.columns or 'rushing_tds' not in data.columns:
        raise ValueError("The DataFrame must contain 'completions' and 'attempts' columns.")
    
    return (data['rushing_yards']*0.1 + data['rushing_tds']*6 + data['rushing_2pt_conversions']*2)

def calculate_completion_percentage(data):
    """
    Calculate completion percentage for all players in the dataset.

    Args:
        data (pd.DataFrame): DataFrame containing 'completions' and 'attempts' columns.

    Returns:
        pd.Series: A Series containing completion percentage for each player.
    """
    if 'completions' not in data.columns or 'attempts' not in data.columns:
        raise ValueError("The DataFrame must contain 'completions' and 'attempts' columns.")
    
    return (data['completions'] / data['attempts']) * 100

# Example: Add more derived metrics here as needed
def calculate_yprr(data):
    """
    Calculate yards per route run for players in the dataset.

    Args:
        data (pd.DataFrame): DataFrame containing 'receiving_yards' and 'routes_run' columns.

    Returns:
        pd.Series: A Series containing yards per route run for each player.
    """
    if 'receiving_yards' not in data.columns or 'routes_run' not in data.columns:
        raise ValueError("The DataFrame must contain 'receiving_yards' and 'routes_run' columns.")
    
    return data['receiving_yards'] / data['routes_run']
