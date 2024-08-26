import requests

mattermost_url = 'https://chat.tsc.uz/api/v4'
mattermost_token = 'bay9pk87mjdmigwjxw4a7t83zr'

headers = {
    'Authorization': f'Bearer {mattermost_token}',
    'Content-Type': 'application/json'
}
CERT_PATH = "Smallstep_Root_CA_40478178306672942733621103581865030166.crt"

# Получение списка всех команд
teams_response = requests.get(f'{mattermost_url}/teams', headers=headers, verify=CERT_PATH)

if teams_response.status_code == 200:
    teams = teams_response.json()
    for team in teams:
        print(f"Team: {team['display_name']}, ID: {team['id']}")
else:
    print(f"Failed to retrieve teams: {teams_response.status_code}, {teams_response.text}")
