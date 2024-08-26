import requests

# Замените на URL вашего Mattermost сервера
BASE_URL = 'https://chat.tsc.uz'
# Токен доступа
TOKEN = '1h79rj6topbkmrbgfwjc6rhzjc'
# Идентификатор плейбука
PLAYBOOK_ID = 'peehdw8rkfraxjc8a4nkjx4wmo'

# Заголовки для авторизации
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}
CERT_PATH = "Smallstep_Root_CA_40478178306672942733621103581865030166.crt"
def get_playbook_status():
    # Endpoint для получения статуса плейбука
    url = f'{BASE_URL}/api/v4/playbooks/{PLAYBOOK_ID}/runs'
    response = requests.get(url, headers=headers, verify=CERT_PATH)

    if response.status_code == 200:
        return response.json()
    else:
        print('Ошибка при получении статуса плейбука:', response.status_code, response.text)
        return None

def print_task_statistics(playbook_status):
    if not playbook_status:
        return

    total_tasks = len(playbook_status.get('tasks', []))
    completed_tasks = sum(1 for task in playbook_status.get('tasks', []) if task['state'] == 'Done')
    incomplete_tasks = total_tasks - completed_tasks

    print(f'Всего задач: {total_tasks}')
    print(f'Выполненных задач: {completed_tasks}')
    print(f'Невыполненных задач: {incomplete_tasks}')

    for task in playbook_status.get('tasks', []):
        if task['state'] != 'Done':
            print(f"Невыполненная задача: {task['title']} - Статус: {task['state']}")

playbook_status = get_playbook_status()
print_task_statistics(playbook_status)
