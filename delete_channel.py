import requests

mattermost_url = 'https://chat.tsc.uz/api/v4'
mattermost_token = '1h79rj6topbkmrbgfwjc6rhzjc'
channel_id = 'kgdooq7tt384fbi3fm4i7orede'
CERT_PATH = "Smallstep_Root_CA_40478178306672942733621103581865030166.crt"
headers = {
    'Authorization': f'Bearer {mattermost_token}',
    'Content-Type': 'application/json'
}

response = requests.delete(f'{mattermost_url}/channels/{channel_id}', headers=headers, verify=CERT_PATH)

if response.status_code == 200:
    print(f'Channel {channel_id} deleted successfully')
else:
    print(f'Failed to delete channel: {response.status_code}, {response.text}')
