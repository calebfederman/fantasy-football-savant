from fetch_data import get_player_info, get_seasonal_data, load_raw_data
from preprocess_data import preprocess_and_save
from lollipop_chart import generate_lollipop_chart
from profiles import QBProfile, RBProfile, WRProfile, TEProfile

# Main workflow
def main():
    # Fetch data
    seasonal_data = get_seasonal_data(years=[2024], season_type='REG')
    player_info = get_player_info()
    
    # Preprocess and save data
    preprocess_and_save(seasonal_data, player_info)
    
    # Get player ID from user
    player_id = input("Enter player ID: ")
    
    # Determine position and load corresponding data
    position = player_info[player_info['gsis_id'] == player_id].iloc[0]['position']
    
    stats_file = {
        'QB': './data/processed/qb_data.csv',
        'RB': './data/processed/rb_data.csv',
        'WR': './data/processed/wr_data.csv',
        'TE': './data/processed/te_data.csv'
    }.get(position)
    
    if stats_file is None:
        raise ValueError(f"Unsupported position: {position}")
    
    stats = load_raw_data(stats_file)
    
    # Create appropriate profile
    profile_class = {
        'QB': QBProfile,
        'RB': RBProfile,
        'WR': WRProfile,
        'TE': TEProfile
    }.get(position)
    
    profile = profile_class(player_id, player_info, stats)
    
    # Get lollipop data
    categories, values, title, subtitle = profile.get_lollipop_data()
    
    # Generate lollipop chart
    generate_lollipop_chart(categories, values, title, subtitle)

if __name__ == "__main__":
    main()
