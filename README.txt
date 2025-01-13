# NFL Player Lollipop Visualization Project

This project visualizes NFL player data using lollipop charts. The goal is to present key metrics for different positions (QB, RB, WR, TE) in an intuitive and visually appealing way, inspired by Baseball Savant's visualization style.

---

## Features

- **Data Fetching**: Fetches seasonal and player information data using `nfl-data-py`.
- **Data Preprocessing**: Calculates key metrics and percentiles based on qualifying players.
- **Position Profiles**: Defines position-specific player profiles (e.g., QB, RB) to organize data and generate insights.
- **Lollipop Charts**: Creates lollipop visualizations for easy comparison of player performance metrics.

---

## Project Structure

```
.
├── .venv/                 # Virtual environment directory
├── data/                  # Raw and processed data
│   ├── raw/               # Raw data files
│   ├── processed/         # Processed data files
├── src/                   # Source code for the project
│   ├── fetch_data.py      # Fetch and save raw data
│   ├── preprocess_data.py # Preprocess data and calculate percentiles
│   ├── profiles.py        # Player profile classes (QB, RB, WR, TE)
│   ├── metrics_utils.py   # Utility functions for metric calculations
│   ├── lollipop_chart.py  # Functions for generating lollipop charts
│   ├── main.py            # Entry point for the project
├── README.txt             # Project overview and instructions
├── requirements.txt       # Python dependencies
```

---

## Prerequisites

- Python 3.8 or higher

---

## Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment**:
   - **Windows**:
     ```bash
     .\.venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Project

1. **Run the Main Script**:
   ```bash
   python src/main.py
   ```

2. **Enter Player ID**:
   When prompted, enter the desired player's ID to generate a lollipop chart visualization.

---

## Example Visualization

Below is a sample lollipop chart generated for an NFL quarterback:

![Lollipop Visualization Example](lollipop_visualization.png)

---

## Acknowledgments

- [nfl-data-py](https://pypi.org/project/nfl-data-py/) for providing easy access to NFL data.
- Inspiration from Baseball Savant's visualization style.

