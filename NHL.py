import requests
import pandas
import matplotlib.pyplot as plt
import numpy as np


#for team_id in range(1, 40):
#    team = requests.get('https://statsapi.web.nhl.com/api/v1/teams/'+ str(team_id))
#    name = team.json()
#    team_name = name['teams'][0]['name']
#    api_endpoint = 'https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(team_id) + '&startDate=2023-10-10&endDate=2024-04-18'
#    response = requests.get(api_endpoint)
#    if response.status_code == 200 and name['teams'][0]['active'] == True:
#        data = response.json()
#        print(team_name, "Schedule")
#    #    print(data)
#        for game_number in range(82):
#            matchup = data['dates'][game_number]['games'][0]['teams']
#            if matchup['away']['team']['name'] != team_name:
#                print('Game ', game_number+1, data['dates'][game_number]['date'], 'vs. ', matchup['away']['team']['name'])
#            else:
#                print('Game ', game_number+1, data['dates'][game_number]['date'], '@ ', matchup['home']['team']['name'])
#
#    else:
#        print("Request failed with status code:", response.status_code)
#
#

# team = requests.get('https://statsapi.web.nhl.com/api/v1/teams/17/roster/')
# data = team.json()

team_ids = [17, 18, 19]  # replace with the actual team IDs
colors = ['red', 'green', 'blue']  # replace with the actual colors you want

# Create an empty DataFrame to store the results
results = pandas.DataFrame(columns=['TOI', 'goals', 'team'])

for team_id, color in zip(team_ids, colors):
    team = requests.get(f'https://statsapi.web.nhl.com/api/v1/teams/{team_id}/roster/')
    data = team.json()

    ids = []
    for player in range(len(data['roster'])):
        if data['roster'][player]['position']['code'] == 'G':
            continue
        else:
            ids.append(data['roster'][player]['person']['id'])

    for player in ids:
        connect = requests.get(f'https://statsapi.web.nhl.com/api/v1/people/{player}/stats?stats=statsSingleSeason&season=20222023')
        stats = connect.json()
        if stats['stats'][0]['splits']:
            toi = (stats['stats'][0]['splits'][0]['stat']['timeOnIcePerGame'])
            toi = int(toi.split(':')[0]) + int(toi.split(':')[1])/60
            num = stats['stats'][0]['splits'][0]['stat']['goals']
            # Append the data to the DataFrame
            results = results.append({'TOI': toi, 'goals': num, 'team': team_id}, ignore_index=True)

# Plot the data
for team_id, color in zip(team_ids, colors):
    team_data = results[results['team'] == team_id]
    plt.scatter(team_data['TOI'], team_data['goals'], color=color)

plt.xticks(np.arange(9, results['TOI'].max()+1, 1))
plt.xlabel('Time On Ice Per Game')  # naming the x axis
plt.ylabel('Total Goals')  # naming the y axis
plt.title('Total Goals vs Time on Ice Per Game')  # giving a title to the graph
plt.show()
