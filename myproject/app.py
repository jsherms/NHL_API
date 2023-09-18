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
        print(selected_team)
        print(selected_type)
        cursor.execute("SELECT id FROM nhl_team WHERE name = ?", (selected_team,))
        team_id = cursor.fetchone()
        print(team_id[0])
    # Connect to the hockey_data database
        if selected_type == 'Schedule':
            print("test2")
            api_endpoint = 'https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(team_id[0]) + '&startDate=2023-10-10&endDate=2024-04-18'
            response = requests.get(api_endpoint)
            schedule = []
            if response.status_code == 200:
                data = response.json()
                for game_number in range(82):
                    matchup = data['dates'][game_number]['games'][0]['teams']
                    if matchup['away']['team']['name'] != selected_team:
                        schedule.append(('Game ' + str(game_number+1) + ' ' + data['dates'][game_number]['date'] + ' vs. ' + matchup['away']['team']['name']))
                    else:
                        schedule.append(('Game ' + str(game_number+1) + ' ' + data['dates'][game_number]['date'] + ' @ ' + matchup['home']['team']['name']))
                return render_template('result.html',  schedule=schedule)
            else:
                print("Request failed with status code:", response.status_code)

    return redirect('/')

@app.route('/schedule', methods=['GET'])
def schedule():
    if request.form.get('type') == 'Schedule':
        print("test2")
        api_endpoint = 'https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(team_id) + '&startDate=2023-10-10&endDate=2024-04-18'
        response = requests.get(api_endpoint)
        schedule = []
        if response.status_code == 200:
            data = response.json()
            for game_number in range(82):
                matchup = data['dates'][game_number]['games'][0]['teams']
                if matchup['away']['team']['name'] != selected_team:
                    schedule.append(('Game ' + str(game_number+1), data['dates'][game_number]['date'] + 'vs. ' + matchup['away']['team']['name']))
                else:
                    schedule.append(('Game ' + str(game_number+1) + data['dates'][game_number]['date'] + '@ ' + matchup['home']['team']['name']))
            print(schedule)
            return render_template('result.html',  schedule=schedule)
        else:
            print("Request failed with status code:", response.status_code)

    return render_template('result.html', team=teams, types=types, filters=filters)

if __name__ == '__main__':
    app.run()