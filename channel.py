import requests

mattermost_url = 'https://chat.tsc.uz'
playbooks_channels_url = f'{mattermost_url}/plugins/playbooks/api/v0/runs/channels'
mattermost_token = '1h79rj6topbkmrbgfwjc6rhzjc'
CERT_PATH = "Smallstep_Root_CA_40478178306672942733621103581865030166.crt"

headers = {
    'Authorization': f'Bearer {mattermost_token}',
    'Content-Type': 'application/json'
}

def get_all_channels():
    response = requests.get(playbooks_channels_url, headers=headers, verify=CERT_PATH)
    if response.status_code == 200:
        print(response.json())

if __name__ == '__main__':
    get_all_channels()
