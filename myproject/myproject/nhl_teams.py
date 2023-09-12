import sqlite3
import requests


conn = sqlite3.connect('myproject/hockey_data.sqlite3')
cursor = conn.cursor()

# Drop the nhl_team table if it exists
cursor.execute("DROP TABLE IF EXISTS nhl_team")

# Create the nhl_team table
cursor.execute("""
    CREATE TABLE nhl_team (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")
               

url = "https://statsapi.web.nhl.com/api/v1/teams?active=true"
response = requests.get(url)
data = response.json()


if response.status_code == 200:
    teams = data["teams"]
    for team in teams:
        team_id = team["id"]
        print(team_id)
        team_name = team["name"]
        print(team_name)
        cursor.execute("SELECT id FROM nhl_team WHERE id = ?", (team_id,))
        existing_id = cursor.fetchone()
        
        if existing_id is None:
            cursor.execute("INSERT INTO nhl_team (id, name) VALUES (?, ?)", (team_id, team_name))
            conn.commit()
        else:
            print(f"Team with id {team_id} already exists in the table.")
else:
    print("Error occurred while making the API request.")


conn.commit()
conn.close()
