import paramiko
import os
import io
from minio import Minio
from minio.error import S3Error
from datetime import timedelta
import requests
import json
import datetime
from flask import Flask, request, jsonify
import time
from pprint import pprint

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

temp_storage = {}
temp_storage2 = {}

# Настройки Mattermost
BASE_URL = 'https://chat.tsc.uz'
TOKEN = 'bay9pk87mjdmigwjxw4a7t83zr'
TEAM_ID = '5o75syrtzjboufgp3rdfxjjrao'
USER_ID = 'e5p8wt1qctds7kschqqjm197wy'
CERT_PATH = "Smallstep_Root_CA_40478178306672942733621103581865030166.crt"
TOKEN_NAUTOBOT = "a74c66e277146e7b4514c4f6cabe339e222547a0"
URL_NAUTOBOT = 'https://10.10.0.249/api/dcim/devices/'
TOKEN_ONCALL = "624263bc7e5d57a58b832d8600c00dd0b5fe905b4cd2cb96bf43e5a1f2ef5a26"
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

headers_nautobot = {
    "Authorization": f"Token {TOKEN_NAUTOBOT}",
    "Accept": "application/json"
}

headers_oncall = {
    "Authorization": f"{TOKEN_ONCALL}",
    "Content-Type": "application/json"
}

SOLVED_CATEGORY_ID = "123"

# Параметры для подключения к удаленному серверу по SSH
ssh_host = '10.10.0.219'
ssh_port = 22
ssh_username = 'root'
ssh_password = 'Insider29'


# Параметры MinIO
minio_client = Minio(
    "10.10.0.210:9000",
    access_key="ecwncAPfrmjJA2LkY08Z",
    secret_key="7BNs8tnBD9G8FmpXS9nbD0dcV1Wp2qELRGiOljtY",
    secure=False
)
bucket_name = "diags"

remote_script_path = 'diagonal'






def create_channel(trigger_name):
    timestamp = datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S')
    channel_name = f"{trigger_name}-{timestamp.replace(' ', '-').replace(':', '-')}".lower()
    channel_data = {
        "team_id": TEAM_ID,
        "name": channel_name,
        "display_name": f"{trigger_name} {timestamp}",
        "type": "O"  # "O" for public channel, "P" for private channel
    }

    create_channel_url = f'{BASE_URL}/api/v4/channels'
    response = requests.post(create_channel_url, headers=headers, json=channel_data, verify=CERT_PATH)

    if response.status_code == 201:
        channel = response.json()
        channel_id = channel['id']
        print('Канал успешно создан с ID:', channel_id)
        return channel_id
    else:
        print('Ошибка при создании канала:', response.status_code, response.text)
        exit(1)


def add_user_to_channel(channel_id):
    add_user_url = f'{BASE_URL}/api/v4/channels/{channel_id}/members'
    add_user_data = {
        "user_id": USER_ID
    }
    response = requests.post(add_user_url, headers=headers, json=add_user_data, verify=CERT_PATH)

    if response.status_code == 201:
        print('Пользователь успешно добавлен в канал.')
    else:
        print('Ошибка при добавлении пользователя в канал:', response.status_code, response.text)
        exit(1)


def send_message_to_channel(channel_id, message, buttons=None):
    message_data = {
        "channel_id": channel_id,
        "message": message,
        "props": {}
    }
    # markdown_message = f"**Alert:** {message}\n\n> [Посетите наш сайт](http://10.10.0.222:3000/s/january/p/aaa-connection-oGoWO2kF0R)"

    # message_data = {
    #     "channel_id": channel_id,
    #     "message": "Нажмите кнопку для теста.",
    #     "props": {
    #         "attachments": [
    #             {
    #                 "text": "Выберите действие:",
    #                 "actions": buttons
    #             }
    #         ]
    #     }
    # }
    if buttons:
        message_data["props"] = {
            "attachments": [{
                "text": "",
                "actions": buttons
            }]
        }

    # if buttons:
    #     message_data["props"] = {
    #         "attachments": [{
    #             "text": message,
    #             "actions": buttons
    #         }]
    #     }

    print("Отправляемый JSON:", json.dumps(message_data, indent=2))
    response = requests.post(f'{BASE_URL}/api/v4/posts', headers=headers, json=message_data, verify=CERT_PATH)

    if response.status_code == 201:
        post_id = response.json()['id']
        print('Сообщение успешно отправлено в канал.')
        return post_id

    else:
        print('Ошибка при отправке сообщения в канал:', response.status_code, response.text)
        print("Ответ Mattermost:", response.text)
        exit(1)



def archive_channel(channel_id):
    archive_url = f'{BASE_URL}/api/v4/channels/{channel_id}'

    response = requests.post(archive_url, headers=headers, verify=CERT_PATH)

    if response.status_code == 200:
        print(f"Канал {channel_id} успешно закрыт (архивирован).")
    else:
        print(f"Ошибка при закрытии (архивировании) канала: {response.status_code}, {response.text}")


def get_host_id(host_name):
    with open("servers.json", 'r') as f:
        hosts_ids = json.load(f)

    if host_name in hosts_ids:
        return hosts_ids[host_name]

    else:
        print(f"ID для хоста '{host_name}' не найден.")
        return None


def get_info_about_server(host_id):
    response = requests.get(f"{URL_NAUTOBOT}{host_id}", headers=headers_nautobot, verify=False)
    if response.status_code == 200:
        data = response.json()
        server_name = data['display']
        serial_number = data['serial']
        asset_tag = data['asset_tag']
        message = (
            f"💻 **Hostname:** `{server_name}`\n"
            f"🔑 **Serial Number:** `{serial_number}`\n"
            f"🏷️ **Asset Tag:** `{asset_tag}`\n"
        )
        return message
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)


@app.route('/alert', methods=['POST'])
def alert_test():
    data = request.json
    message = f"{data['alert_payload']['message']} is firing"
    print(message.split(" "))
    host_name = message.split(" ")[0]
    alert_group_id = data['alert_group_id']
    temp_storage[host_name] = alert_group_id
    # pprint(data)
    host_id = get_host_id(host_name)
    # print(host_id)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

        # Выполнение скрипта для генерации файла
        stdin, stdout, stderr = ssh_client.exec_command(f'{remote_script_path}')
        stdout.channel.recv_exit_status()

        # Получение имени созданного файла
        generated_file_name = stdout.readlines()[-1].strip().split(' ')[1]

        # Скачивание файла с удаленного сервера
        sftp_client = ssh_client.open_sftp()
        local_file_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\grafana\\files', generated_file_name)
        sftp_client.get(generated_file_name, local_file_path)
        sftp_client.close()

        # Загрузка файла в MinIO
        with open(local_file_path, 'rb') as file_data:
            file_stat = os.stat(local_file_path)
            minio_client.put_object(bucket_name, generated_file_name, io.BytesIO(file_data.read()),
                                    length=file_stat.st_size)

        # Получение ссылки для скачивания
        url = minio_client.presigned_get_object(bucket_name, generated_file_name, expires=timedelta(hours=1))
        print(f'Download link: {url}')

    finally:
        ssh_client.close()


    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # alert_message = f"**Alert:** test at {timestamp}\n\n> {message}"  # Старый вид сообщения
    alert_message = f"# Alert: test at {timestamp}\n\n🔥🔥🔥 {message}"
    # channel_id = create_channel(trigger_name)
    channel_id = create_channel("Alert")

    buttons = [
        {
            "name": "Acknowledged",
            "integration": {
                "url": "http://10.10.1.54:5000/acknowledged",
                "context": {
                    "action": "acknowledged",
                    "channel_id": channel_id,
                    "host_name": host_name
                }
            },
            "type": "button",
            "style": "default"
        }
        # {
        #     "name": "Not success",
        #     "integration": {
        #         "url": "http://10.10.1.51:5000/notsuccess",
        #         "context": {
        #             "action": "notsuccess",
        #             "channel_id": channel_id
        #         }
        #     },
        #     "type": "button",
        #     "style": "default"
        # }
    ]

    add_user_to_channel(channel_id)
    post_id = send_message_to_channel(channel_id, alert_message, buttons)
    print(post_id)
    temp_storage2['test'] = post_id
    info_about_server = get_info_about_server(host_id)
    send_message_to_channel(channel_id, info_about_server)
    send_message_to_channel(channel_id, f"## [Скачать diagonal]({url})")

    # status_message = restart_nginx_and_get_status()
    # send_message_to_channel(channel_id, status_message, buttons)

    return jsonify({"status": "success"}), 200


@app.route('/solved', methods=['POST'])
def solved():
    channel_id = request.form.get('channel_id')
    print(channel_id)

    if not channel_id:
        return jsonify({"error": "channel_id is required"}), 400

    archive_channel(channel_id)

    return jsonify({"status": "success"}), 200


@app.route('/acknowledged', methods=['POST'])
def acknowledged():
    data = request.json
    host_name = data.get("context", {}).get("host_name")
    channel_id = data.get("context", {}).get("channel_id")
    # post_id = data.get("context", {}).get("post_id")

    alert_group_id = temp_storage.get(host_name)
    print(alert_group_id)
    if not alert_group_id:
        return jsonify({"status": "error", "message": "alert_group_id not found"}), 404
    oncall_api_url = f"http://10.10.0.238:8080/api/v1/alert_groups/{alert_group_id}/acknowledge"

    response = requests.post(oncall_api_url, headers=headers_oncall)
    send_message_to_channel(channel_id, "Дежурный ознакомился 🫡")
    post_id = temp_storage2.get('test')
    print(post_id)

    if response.status_code == 200:
        # Новое сообщение без кнопки
        new_message = f"🚨 Alert acknowledged."

        update_message(channel_id, post_id, new_message)
        send_message_to_channel(channel_id, "## [Статья здесь](http://10.10.0.222:3000/s/january/p/aaa-connection-oGoWO2kF0R)")
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error"}), response.status_code


def update_message(channel_id, post_id, new_message):
    update_data = {
        "id": post_id,
        "channel_id": channel_id,
        "message": new_message,
        "props": {}  # Удаляем props, чтобы убрать кнопки
    }

    response = requests.put(f'{BASE_URL}/api/v4/posts/{post_id}', headers=headers, json=update_data, verify=CERT_PATH)

    if response.status_code == 200:
        print('Сообщение успешно обновлено.')
    else:
        print('Ошибка при обновлении сообщения:', response.status_code, response.text)

    # return jsonify({"status_code": response.status_code}), response.status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
