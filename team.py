import requests
import json

# URL Mattermost сервера
base_url = 'https://chat.tsc.uz'

# Токен доступа
access_token = '1h79rj6topbkmrbgfwjc6rhzjc'

# Заголовки
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

CERT_PATH = "Smallstep_Root_CA_40478178306672942733621103581865030166.crt"

# URL для получения списка команд
get_teams_url = f'{base_url}/api/v4/teams'

# Выполнение запроса
response = requests.get(get_teams_url, headers=headers, verify=CERT_PATH)

if response.status_code == 200:
    teams = response.json()
    for team in teams:
        print(f"ID: {team['id']}, Name: {team['name']}")
else:
    print('Failed to retrieve teams')
    print(response.status_code, response.text)
