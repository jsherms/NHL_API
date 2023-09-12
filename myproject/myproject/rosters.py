import sqlite3
import requests

conn = sqlite3.connect('myproject/myproject/hockey_data.sqlite3')
cursor = conn.cursor()

# Drop the nhl_team table if it exists
cursor.execute("DROP TABLE IF EXISTS player")

# Create the nhl_team table
cursor.execute("""
    CREATE TABLE player (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        jersey_number INTEGER,
        team_id INTEGER,
        FOREIGN KEY (team_id) REFERENCES nhl_team (id)
        );
""")
# Retrieve team IDs from the NHL_teams table
cursor.execute("SELECT id FROM nhl_team")
team_ids = cursor.fetchall()

# Create an empty list to store player data
player_data = []

# Loop through each team ID
for team_id in team_ids:
    team_id = team_id[0]  # Extract the team ID from the tuple
    
    # Make API request to retrieve roster data for the team
    team = requests.get(f'https://statsapi.web.nhl.com/api/v1/teams/{team_id}/roster/')
    data = team.json()
    
    # Loop through each player in the roster data
    for player in data['roster']:
        if 'jerseyNumber' not in player or player['jerseyNumber'] is None:
            continue
        player_id = player['person']['id']
        player_name = player['person']['fullName']
        position_abbreviation = player['position']['abbreviation']
        jersey_number = player['jerseyNumber']
        
        # Append player data to the list
        player_data.append((player_id, player_name, position_abbreviation, jersey_number, team_id))

# Insert player data into the player table
cursor.executemany("INSERT INTO player (id, name, position, jersey_number, team_id) VALUES (?, ?, ?, ?, ?)", player_data)
conn.commit()

conn.close()