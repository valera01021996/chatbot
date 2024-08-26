import requests

mattermost_url = 'https://chat.tsc.uz/api/v4'
mattermost_token = 'bay9pk87mjdmigwjxw4a7t83zr'

headers = {
    'Authorization': f'Bearer {mattermost_token}',
    'Content-Type': 'application/json'
}

response = requests.get(f'{mattermost_url}/users', headers=headers, verify=False)

if response.status_code == 200:
    users = response.json()
    for user in users:
        print(f"User: {user['username']}, ID: {user['id']}")
else:
    print(f"Failed to retrieve users: {response.status_code}, {response.text}")


# import requests
#
# mattermost_url = 'https://chat.tsc.uz/api/v4'
# mattermost_token = '968rzka6tpbn789remx7zmc3ge'
#
# headers = {
#     'Authorization': f'Bearer {mattermost_token}',
#     'Content-Type': 'application/json'
# }
#
# response = requests.get(f'{mattermost_url}/teams', headers=headers, verify=False)
#
# if response.status_code == 200:
#     teams = response.json()
#     for team in teams:
#         print(f"Team: {team['name']}, ID: {team['id']}")
# else:
#     print(f"Failed to retrieve teams: {response.status_code}, {response.text}")
