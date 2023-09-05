import requests
import pandas
import matplotlib.pyplot as plt
import numpy as np


team_ids = [17, 18, 19]  
colors = ['red', 'green', 'blue'] 

# Create an empty DataFrame to store the results
results = pandas.DataFrame(columns=['TOI', 'goals', 'team', 'player'])

for team_id, color in zip(team_ids, colors):
    team = requests.get(f'https://statsapi.web.nhl.com/api/v1/teams/{team_id}/roster/')
    data = team.json()

    ids = {}
    for player in range(len(data['roster'])):
        if data['roster'][player]['position']['code'] == 'G':
            continue
        else:
            player_id = data['roster'][player]['person']['id']
            player_name = data['roster'][player]['person']['fullName']
            ids[player_id] = player_name

    for player_id, player_name in ids.items():
        connect = requests.get(f'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season=20222023')
        stats = connect.json()
        if stats['stats'][0]['splits']:
            toi = (stats['stats'][0]['splits'][0]['stat']['timeOnIcePerGame'])
            toi = int(toi.split(':')[0]) + int(toi.split(':')[1])/60
            num = stats['stats'][0]['splits'][0]['stat']['goals']
            # Append the data to the DataFrame
            results.loc[len(results)] = [toi, num, team_id, player_name]

# Plot the data
for team_id, color in zip(team_ids, colors):
    team_data = results[results['team'] == team_id]
    plt.scatter(team_data['TOI'], team_data['goals'], color=color)
    if color == 'red':
        for i in range(len(team_data)):
            plt.annotate(team_data.iloc[i]['player'], (team_data.iloc[i]['TOI'], team_data.iloc[i]['goals']))

plt.xticks(np.arange(9, results['TOI'].max()+1, 1))
plt.xlabel('Time On Ice Per Game')  # naming the x axis
plt.ylabel('Total Goals')  # naming the y axis
plt.title('Total Goals vs Time on Ice Per Game')  # giving a title to the graph
plt.show()
