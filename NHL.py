import requests

api_endpoint = 'https://statsapi.web.nhl.com/api/v1/people/8481542'
response = requests.get(api_endpoint)

if response.status_code == 200:
    data = response.json()
    print("Response data:")
    print(data)
else:
    print("Request failed with status code:", response.status_code)
