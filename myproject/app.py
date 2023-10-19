from flask import Flask, render_template, request, redirect, session
import sqlite3
import requests
from datetime import date
import calendar
app = Flask(__name__)
app.secret_key = 'pickles'

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
    return render_template('index.html', teams=teams, default_team='Anaheim Ducks')


@app.route('/submit', methods= ['GET', 'POST'])
def submit():
    if request.method == 'POST':
        selected_team = request.form.get('teams')
        session['selected_team'] = selected_team
        session['month'] = date.today().month
        session['year'] = date.today().year

        conn = sqlite3.connect('hockey_data.sqlite3')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM nhl_team WHERE name = ?", (selected_team,))
        team_id = cursor.fetchone()
    # Connect to the hockey_data database
       
        schedule, month = get_schedule(team_id[0], 0)
        
        return render_template('schedule.html',  schedule=schedule, teams=teams, default_team=selected_team, month=month)
    return redirect('/')

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    if request.method == 'GET':
        return render_template('stats.html', teams=teams)
    else:
        team = request.form.get('teams')
        conn = sqlite3.connect('hockey_data.sqlite3')
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM nhl_team WHERE name = ?", (team,))
        team_id = cursor.fetchone()
        selected_filters = request.form.getlist('filter[]')

        cursor.execute("SELECT {} FROM skater_stats JOIN player ON skater_stats.player_id = player.id WHERE player.team_id = ? ORDER BY points DESC".format(", ".join(selected_filters)), (team_id[0],))
        data = cursor.fetchall()
       

        # Render the template with the filtered stats data
        return render_template('stats.html', teams=teams, stats=data, default_team=team, columns=selected_filters)

@app.route('/get_schedule', methods=['POST'])
def get_schedule(team, num):
    today = date.today()
    # start_date = date(today.year, today.month, 1)
    # end_date = date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    month = session['month']
    year = session['year']
    # if month == None:
    #     month = today.month
    # else:
    #     if month == 12:
    #         month = 1
    #         year = today.year + 1
    #     else:
    #         month += 1
    if num == 0:
        month = today.month
    elif num == 1:
        if month == 12:
            month = 1
            year = today.year + 1
        else:
            month += 1
    else:
        if month == 1:
            month = 12
            year = year - 1
        else:
            month = month - 1
    session['month'] = month
    session['year'] = year
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    # Format the start and end dates as strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    api_endpoint = f'https://statsapi.web.nhl.com/api/v1/schedule?teamId={str(team)}&startDate={start_date_str}&endDate={end_date_str}'
    response = requests.get(api_endpoint)

    if response.status_code == 200:
        data = response.json()
        schedule = []
        for game_number in range((data['totalGames'])):                
            game_info = {
                'Game Number': game_number + 1,
                'Game Date': data['dates'][game_number]['date'],
                'Home Team': data['dates'][game_number]['games'][0]['teams']['home']['team']['name'],
                'Away Team': data['dates'][game_number]['games'][0]['teams']['away']['team']['name']
            }
            schedule.append(game_info)
        return schedule, month
        # Now, you can work with the schedule_data to access the game schedule for the current month.
        
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


@app.route('/next', methods=['POST'])
def next_month():
    # Logic to calculate the next month
    # You can use the datetime module to increment the current month
    # and update the 'current_month' variable for the template

    selected_team = request.form.get('teams')
    if selected_team == None:
        selected_team = session['selected_team']

    conn = sqlite3.connect('hockey_data.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM nhl_team WHERE name = ?", (selected_team,))
    team_id = cursor.fetchone()
    print(session['month'])
    # Render the template with the updated month
    schedule, month = get_schedule(team_id[0], 1)
    return render_template('schedule.html',  schedule=schedule, teams=teams, default_team=selected_team, current_month=month)

@app.route('/previous', methods=['POST'])
def previous_month():
    # Logic to calculate the previous month
    # You can use the datetime module to decrement the current month
    # and update the 'current_month' variable for the template

    # Render the template with the updated month
    selected_team = request.form.get('teams')
    if selected_team == None:
        selected_team = session['selected_team']

    conn = sqlite3.connect('hockey_data.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM nhl_team WHERE name = ?", (selected_team,))
    team_id = cursor.fetchone()
    print(session['month'])
    # Render the template with the updated month
    schedule, month = get_schedule(team_id[0], -1)
    return render_template('schedule.html',  schedule=schedule, teams=teams, default_team=selected_team, current_month=month)

@app.route('/<path:path>')
def catch_all(path='index.html'):
    return render_template(path)

if __name__ == '__main__':
    app.run()