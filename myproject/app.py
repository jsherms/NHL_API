from flask import Flask, render_template, request, redirect
import sqlite3
import requests
app = Flask(__name__)

conn = sqlite3.connect('hockey_data.sqlite3')
cursor = conn.cursor()
   
cursor.execute("SELECT name FROM nhl_team")
teams = [row[0] for row in cursor.fetchall()]
teams.sort()

# Close the database connection
cursor.close()
conn.close()

types = ['Schedule', 'Data']
filters = ['All', 'Home Only', 'Away Only']

@app.route('/')
def index():

    conn = sqlite3.connect('hockey_data.sqlite3')
    cursor = conn.cursor()
   
    cursor.execute("SELECT name FROM nhl_team")
    teams = [row[0] for row in cursor.fetchall()]
    teams.sort()

    # Close the database connection
    cursor.close()
    conn.close()

    types = ['Schedule', 'Data']
    filters = ['All', 'Home Only', 'Away Only']
    return render_template('index.html', teams=teams, types=types, filters=filters, default_team='Anaheim Ducks', default_type='Schedule', default_filter='All')


@app.route('/submit', methods= ['GET', 'POST'])
def submit():
    if request.method == 'POST':
        selected_team = request.form.get('teams')
        selected_type = request.form.get('type')
        selected_filter = request.form.get('filter')

        conn = sqlite3.connect('hockey_data.sqlite3')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM nhl_team WHERE name = ?", (selected_team,))
        team_id = cursor.fetchone()
    # Connect to the hockey_data database
        if selected_type == 'Schedule':
            api_endpoint = 'https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(team_id[0]) + '&startDate=2023-10-10&endDate=2024-04-18'
            response = requests.get(api_endpoint)
            schedule = []
            if response.status_code == 200:
                data = response.json()
                for game_number in range(82):                
                    game_info = {
                        'Game Number': game_number + 1,
                        'Game Date': data['dates'][game_number]['date'],
                        'Home Team': data['dates'][game_number]['games'][0]['teams']['home']['team']['name'],
                        'Away Team': data['dates'][game_number]['games'][0]['teams']['away']['team']['name']
                    }
                    if selected_filter == 'Home Only':
                        if game_info['Home Team'] != selected_team:
                            continue
                    elif selected_filter == 'Away Only':
                        if game_info['Away Team'] != selected_team:
                            continue
                    schedule.append(game_info)
                return render_template('result.html',  schedule=schedule, teams=teams, types=types, filters=filters, default_team=selected_team, default_type=selected_type, default_filter=selected_filter)
            else:
                print("Request failed with status code:", response.status_code)
        else:
            cursor.execute('SELECT * FROM player WHERE team_id = ?', (team_id[0],))
            data = cursor.fetchall()
            roster = []
            for player in data:
                player = {
                    'Name': player[1],
                    'Position': player[2],
                    'Jersey Number': player[3]
                }
                roster.append(player)
                roster = sorted(roster, key = lambda x: x['Jersey Number'])
            return render_template('roster.html', roster=roster, teams=teams, types=types, filters=filters, default_team=selected_team, default_type=selected_type, default_filter=selected_filter )
    return redirect('/')

@app.route('/<path:path>')
def catch_all(path='index.html'):
    return render_template(path)

if __name__ == '__main__':
    app.run()