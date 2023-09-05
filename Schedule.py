import requests

for team_id in range(1, 40):
   team = requests.get('https://statsapi.web.nhl.com/api/v1/teams/'+ str(team_id))
   name = team.json()
   team_name = name['teams'][0]['name']
   api_endpoint = 'https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(team_id) + '&startDate=2023-10-10&endDate=2024-04-18'
   response = requests.get(api_endpoint)
   if response.status_code == 200 and name['teams'][0]['active'] == True:
       data = response.json()
       print(team_name, "Schedule")
   #    print(data)
       for game_number in range(82):
           matchup = data['dates'][game_number]['games'][0]['teams']
           if matchup['away']['team']['name'] != team_name:
               print('Game ', game_number+1, data['dates'][game_number]['date'], 'vs. ', matchup['away']['team']['name'])
           else:
               print('Game ', game_number+1, data['dates'][game_number]['date'], '@ ', matchup['home']['team']['name'])

   else:
       print("Request failed with status code:", response.status_code)



team = requests.get('https://statsapi.web.nhl.com/api/v1/teams/17/roster/')
data = team.json()