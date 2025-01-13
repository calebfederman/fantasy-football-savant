import pandas as pd
import logging
import metrics_utils
from metrics_utils import calculate_percentile_from_qualifying

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PlayerProfile:
    def __init__(self, player_id, player_info, player_stats):
        self.player_id = player_id
        self.metadata = player_info[player_info['gsis_id'] == player_id].iloc[0]
        self.stats = player_stats[player_stats['player_id'] == player_id]
        self.all_stats = player_stats.copy()  # Create a copy to avoid shared state

        self.name = self.metadata['name']
        self.position = self.metadata['position']
        self.team = self.metadata['team']
        self.age = round(self.metadata['age'])
        self.height = metrics_utils.format_height(self.metadata['height'])
        self.weight = round(self.metadata['weight'])


    def get_lollipop_data(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

class QBProfile(PlayerProfile):
    def get_lollipop_data(self):
        # Calculate necessary metrics
        self.all_stats['passing_fantasy_points'] = metrics_utils.calculate_passing_fantasy_points(self.all_stats)
        self.all_stats['rushing_fantasy_points'] = metrics_utils.calculate_rushing_fantasy_points(self.all_stats)
        self.all_stats['completion_percentage'] = metrics_utils.calculate_completion_percentage(self.all_stats)
        
        # Get the player's row index in `self.all_stats`
        player_row_index = self.all_stats[self.all_stats['player_id'] == self.player_id].index[0]

        categories = {
            'Fantasy Value': ['Fantasy Pts', 'Pass Pts', 'Rush Pts'],
            'Passing': ['Pass Yds', 'Pass TDs', 'Ints', 'Cmp %', 'Pass Att'],
            'Rushing': ['Rush Yds', 'Rush TDs', 'Rush Att']
        }

        values = {
            'Fantasy Value': [
                calculate_percentile_from_qualifying(self.all_stats, 'fantasy_points_ppr', 'attempts', 135).iloc[player_row_index],
                calculate_percentile_from_qualifying(self.all_stats, 'passing_fantasy_points', 'attempts', 135).iloc[player_row_index],
                calculate_percentile_from_qualifying(self.all_stats, 'rushing_fantasy_points', 'attempts', 135).iloc[player_row_index]
            ],
            'Passing': [
                calculate_percentile_from_qualifying(self.all_stats, 'passing_yards', 'attempts', 135).iloc[player_row_index],
                calculate_percentile_from_qualifying(self.all_stats, 'passing_tds', 'attempts', 135).iloc[player_row_index],
                100 - calculate_percentile_from_qualifying(self.all_stats, 'interceptions', 'attempts', 135).iloc[player_row_index],
                calculate_percentile_from_qualifying(self.all_stats, 'completion_percentage', 'attempts', 135).iloc[player_row_index],
                calculate_percentile_from_qualifying(self.all_stats, 'attempts', 'attempts', 135).iloc[player_row_index]
            ],
            'Rushing': [
                calculate_percentile_from_qualifying(self.all_stats, 'rushing_yards', 'attempts', 135).iloc[player_row_index],
                calculate_percentile_from_qualifying(self.all_stats, 'rushing_tds', 'attempts', 135).iloc[player_row_index],
                calculate_percentile_from_qualifying(self.all_stats, 'carries', 'attempts', 135).iloc[player_row_index]
            ]
        }

        title = f'{self.name} 2024'
        subtitle = f'{self.position} | {self.team} | {self.height} {self.weight}LBS | Age: {self.age}'
        
        logging.info(f"Lollipop data prepared for: {self.name}")
        return categories, values, title, subtitle


class RBProfile(PlayerProfile):
    def get_lollipop_data(self):
        
        categories = {
            'Fantasy Value': ['Fantasy Pts', 'Rush Pts', 'Rec Pts'],
            'Rushing': ['Rush Yds', 'Rush TDs', 'Rush Att'],
            'Receiving': ['Rec Yds', 'Rec TDs', 'Targets']
        }
        
        values = {
            'Fantasy Value': [
                self.stats['fantasy_points_ppr_percentile'].iloc[0],
                self.stats['rushing_epa_percentile'].iloc[0],
                self.stats['receiving_epa_percentile'].iloc[0]
            ],
            'Rushing': [
                self.stats['rushing_yards_percentile'].iloc[0],
                self.stats['rushing_tds_percentile'].iloc[0],
                self.stats['carries_percentile'].iloc[0]
            ],
            'Receiving': [
                self.stats['receiving_yards_percentile'].iloc[0],
                self.stats['receiving_tds_percentile'].iloc[0],
                self.stats['targets_percentile'].iloc[0]
            ]
        }
        
        title = f'{self.name} 2024'
        subtitle = f'{self.position} | {self.team} | {self.height} {self.weight}LBS | Age: {self.age}'
        
        logging.info(f"Lollipop data prepared for: {self.name}")
        return categories, values, title, subtitle


class WRProfile(PlayerProfile):
    def get_lollipop_data(self):
        categories = {
            'Fantasy Value': ['Fantasy Pts', 'Rec Pts'],
            'Receiving': ['Rec Yds', 'Rec TDs', 'Targets', 'Air Yds Share']
        }
        
        values = {
            'Fantasy Value': [
                self.stats['fantasy_points_ppr_percentile'].iloc[0],
                self.stats['receiving_epa_percentile'].iloc[0]
            ],
            'Receiving': [
                self.stats['receiving_yards_percentile'].iloc[0],
                self.stats['receiving_tds_percentile'].iloc[0],
                self.stats['targets_percentile'].iloc[0],
                self.stats['air_yards_share_percentile'].iloc[0]
            ]
        }
        
        title = f'{self.name} 2024'
        subtitle = f'{self.position} | {self.team} | {self.height} {self.weight}LBS | Age: {self.age}'
        
        logging.info(f"Lollipop data prepared for: {self.name}")
        return categories, values, title, subtitle


class TEProfile(WRProfile):
    # Inherits get_lollipop_data from WRProfile
    def get_lollipop_data(self):
        return super().get_lollipop_data()
