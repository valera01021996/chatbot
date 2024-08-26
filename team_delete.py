import requests

mattermost_url = 'https://chat.tsc.uz/api/v4'
mattermost_token = 'pswsoocyyp8p98pf3megotgafc'
team_id = '4qb158wo8j8yp8iusok44a1joc'

headers = {
    'Authorization': f'Bearer {mattermost_token}',
    'Content-Type': 'application/json'
}

response = requests.delete(f'{mattermost_url}/teams/{team_id}', headers=headers, verify=False)

if response.status_code == 200:
    print(f'Team {team_id} deleted successfully')
else:
    print(f'Failed to delete team: {response.status_code}, {response.text}')
