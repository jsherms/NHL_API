import sqlite3
import requests

conn = sqlite3.connect('myproject/hockey_data.sqlite3')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS skater_stats")

cursor.execute("""
    CREATE TABLE skater_stats (
        player_id INTEGER PRIMARY KEY,
        name TEXT,
        time_on_ice TEXT,
        games INTEGER,
        goals INTEGER,
        assists INTEGER,
        points INTEGER,
        shots INTEGER,
        hits INTEGER,
        power_play_goals INTEGER,
        power_play_points INTEGER,
        penalty_minutes INTEGER,
        faceoff_pct REAL,
        shot_pct REAL,
        game_winning_goals INTEGER,
        overtime_goals INTEGER,
        short_handed_goals INTEGER,
        short_handed_points INTEGER,
        blocked INTEGER,
        plus_minus INTEGER,
        shifts INTEGER,
        FOREIGN KEY (player_id) REFERENCES player (id)
        );
""")

cursor.execute("SELECT id from player WHERE position != 'G'")
ids = cursor.fetchall()

api_url = "https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season=20222023"
for id in ids:
    print(id[0])
    url = api_url.format(player_id=id[0])
    response = requests.get(url)
    stats = response.json()
    if not stats['stats'][0]['splits']:
        print(id)
        continue
    skater_stats = stats['stats'][0]['splits'][0]['stat']
    cursor.execute("SELECT name FROM player WHERE id = ?", (id[0],))
    result = cursor.fetchone()
    # Retrieve the player's name
    player_name = result[0]
    cursor.execute("""
        INSERT INTO skater_stats (
            player_id, name, time_on_ice, games, goals, assists, points, shots, hits, power_play_goals, 
            power_play_points, penalty_minutes, faceoff_pct, shot_pct, game_winning_goals, overtime_goals, 
            short_handed_goals, short_handed_points, blocked, plus_minus, shifts
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        id[0], player_name, skater_stats['timeOnIce'], skater_stats['games'], 
        skater_stats['goals'], skater_stats['assists'], skater_stats['points'], skater_stats['shots'], 
        skater_stats['hits'], skater_stats['powerPlayGoals'], skater_stats['powerPlayPoints'], 
        skater_stats['penaltyMinutes'], skater_stats['faceOffPct'], skater_stats['shotPct'], 
        skater_stats['gameWinningGoals'], skater_stats['overTimeGoals'], skater_stats['shortHandedGoals'], 
        skater_stats['shortHandedPoints'], skater_stats['blocked'], skater_stats['plusMinus'], 
        skater_stats['shifts']
    ))

conn.commit()
conn.close()