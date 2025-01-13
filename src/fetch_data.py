import nfl_data_py as nfl
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# File paths for saving raw data
SEASONAL_DATA_DIR = './data/raw/'  # Directory for seasonal data
PLAYER_INFO_DIR = './data/raw/'    # Directory for player info data

def ensure_directory_exists(filepath):
    """
    Ensure the directory for the given filepath exists.
    Creates parent directories if they do not already exist.
    """
    dir_path = os.path.dirname(filepath)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logging.info(f"Created directory: {dir_path}")


def get_seasonal_data(years, season_type='REG'):
    """
    Fetch and save seasonal data for the specified years and season type.
    
    Args:
        years (list): List of years to fetch data for (e.g., [2024]).
        season_type (str): Season type, e.g., 'REG' for regular season, 'POST' for postseason. Default is 'REG'.
    
    Returns:
        pd.DataFrame: Seasonal data as a DataFrame.
    """
    try:        
        # Fetch seasonal data from nfl-data-py
        seasonal_data = nfl.import_seasonal_data(years, season_type)
        if seasonal_data.empty:
            logging.warning(f"No seasonal data fetched for years: {years} and season_type: {season_type}")
        
        # Ensure the output directory exists
        ensure_directory_exists(SEASONAL_DATA_DIR)
        
        # Save the data to a CSV file
        output_path = f'{SEASONAL_DATA_DIR}seasonal_data.csv'
        seasonal_data.to_csv(output_path, index=False)
        
        # Check if data was saved properly
        if os.path.exists(output_path):
            logging.info(f"File successfully saved to: {os.path.abspath(output_path)}")
        else:
            logging.error(f"Failed to save file: {output_path}")
            
        return seasonal_data
    except Exception as e:
        # Log any errors and return an empty DataFrame
        logging.error(f"Error fetching seasonal data: {e}")
        return pd.DataFrame()

def get_player_info():
    """
    Fetch and save player information data.
    
    Returns:
        pd.DataFrame: Player information as a DataFrame.
    """
    try:
        # Fetch player info from nfl-data-py
        player_info = nfl.import_ids()
        if player_info.empty:
            logging.warning(f"No player info data fetched")
        
        # Ensure the output directory exists
        ensure_directory_exists(PLAYER_INFO_DIR)
        
        # Save the data to a CSV file
        output_path = f'{PLAYER_INFO_DIR}player_info.csv'
        player_info.to_csv(output_path, index=False)
        
        # Check if data was saved properly
        if os.path.exists(output_path):
            logging.info(f"File successfully saved to: {os.path.abspath(output_path)}")
        else:
            logging.error(f"Failed to save file: {output_path}")
            
        return player_info
    except Exception as e:
        # Log any errors and return an empty DataFrame
        logging.error(f"Error fetching player info: {e}")
        return pd.DataFrame()

def load_raw_data(filepath):
    """
    Load raw data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    try:
        # Attempt to load the CSV file
        logging.info(f"Loading data from {filepath}...")
        return pd.read_csv(filepath)
    except FileNotFoundError:
        # Log an error if the file does not exist and return an empty DataFrame
        logging.error(f"File not found: {filepath}")
        return pd.DataFrame()
