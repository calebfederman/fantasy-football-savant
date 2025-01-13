import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directory for saving processed data
PROCESSED_DATA_DIR = './data/processed/'

def ensure_directory_exists(filepath):
    """
    Ensure the directory for the given filepath exists.
    Creates parent directories if they do not already exist.
    
    Args:
        filepath (str): The path where the file will be saved.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

def load_raw_data(filepath):
    """
    Load raw data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    try:
        logging.info(f"Loading data from {filepath}...")
        return pd.read_csv(filepath)
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return pd.DataFrame()

def filter_player_info(player_info):
    """
    Filter player information to include only relevant positions and columns.
    
    Args:
        player_info (pd.DataFrame): DataFrame containing player information.
        
    Returns:
        pd.DataFrame: Filtered player info including only QB, RB, WR, and TE positions.
    """
    relevant_columns = ['gsis_id', 'name', 'position', 'team', 'height', 'weight', 'age', 'college']
    return player_info[relevant_columns][player_info['position'].isin(['QB', 'RB', 'WR', 'TE'])].reset_index(drop=True)

def merge_data(seasonal_data, player_info):
    """
    Merge seasonal data with filtered player information.
    
    Args:
        seasonal_data (pd.DataFrame): Raw seasonal data.
        filtered_player_info (pd.DataFrame): Filtered player information.
        
    Returns:
        pd.DataFrame: Merged data containing seasonal stats and player info.
    """
    return player_info.merge(seasonal_data, left_on='gsis_id', right_on='player_id', how='right')

def filter_qualifying_players(data, position, qualifying_stat, min_attempts):
    """
    Filter qualifying and non-qualifying players for a given position.

    Args:
        data (pd.DataFrame): The DataFrame containing player data.
        position (str): The position to filter (e.g., 'QB').
        qualifying_stat (str): The stat to use for qualification (e.g., 'passing_attempts').
        min_attempts (int): Minimum attempts required to qualify.

    Returns:
        tuple: (qualifying_players, non_qualifying_players)
    """
    qualifying = data[(data['position'] == position) & (data[qualifying_stat] >= min_attempts)]
    non_qualifying = data[(data['position'] == position) & (data[qualifying_stat] < min_attempts)]
    return qualifying, non_qualifying

def preprocess_and_save(seasonal_data, player_info):
    """
    Preprocess raw data for all positions, including filtering and merging.
    
    Args:
        seasonal_data (pd.DataFrame): Raw seasonal data.
        player_info (pd.DataFrame): Player information data.
    """
    ensure_directory_exists(PROCESSED_DATA_DIR)
    
    # Filter and merge data
    filtered_player_info = filter_player_info(player_info)
    merged_data = merge_data(seasonal_data, filtered_player_info)
    
    # Define position-specific qualification criteria
    qualifications = {
        'QB': {'stat': 'attempts', 'min_attempts': 135},
        'RB': {'stat': 'carries', 'min_attempts': 90},
        'WR': {'stat': 'targets', 'min_attempts': 45},
        'TE': {'stat': 'targets', 'min_attempts': 45}
    }
    
    # Process each position
    for position, criteria in qualifications.items():
        qualifying, non_qualifying = filter_qualifying_players(
            merged_data, position, criteria['stat'], criteria['min_attempts']
        )
        
        # Combine qualifying and non-qualifying players
        combined_data = pd.concat([qualifying, non_qualifying])
        
        # Save processed data for each position
        output_path = f"{PROCESSED_DATA_DIR}{position.lower()}_data.csv"
        combined_data.to_csv(output_path, index=False)
        logging.info(f"Processed {position} data saved to {output_path}.")
