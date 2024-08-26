import requests

# Замените на URL вашего Mattermost сервера
BASE_URL = 'https://chat.tsc.uz'
# Токен доступа
TOKEN = '1h79rj6topbkmrbgfwjc6rhzjc'

# Заголовки для авторизации
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}
CERT_PATH = "Smallstep_Root_CA_40478178306672942733621103581865030166.crt"
# Данные нового пользователя
new_user_data = {
    'email': 'jasur@tashsoftcom.uz',
    'username': 'jasur',
    'password': 'password123',
    'first_name': 'Jasur',
    'last_name': 'Abdurasulov'
}

# Endpoint для создания нового пользователя
url = f'{BASE_URL}/api/v4/users'

# Отправка POST запроса для создания нового пользователя
response = requests.post(url, headers=headers, json=new_user_data, verify=CERT_PATH)

if response.status_code == 201:
    print('Пользователь успешно создан.')
    print('Детали пользователя:', response.json())
else:
    print('Ошибка при создании пользователя:', response.status_code, response.text)
