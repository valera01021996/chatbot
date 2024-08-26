import requests

# Замените на ваши данные
# oncall_api_url = "http://10.10.0.238:8080/api/v1/alerts/"
oncall_api_url = "http://10.10.0.238:8080/api/v1/alert_groups/I7XGUUZWYWE9Y/acknowledge"
alert_id = "I7XGUUZWYWE9Y"
api_key = "624263bc7e5d57a58b832d8600c00dd0b5fe905b4cd2cb96bf43e5a1f2ef5a26"

# Заголовки запроса
headers = {
    "Authorization": f"{api_key}",
    "Content-Type": "application/json"
}

# Тело запроса для изменения статуса
data = {
    "status": "Acknowledged"
}

# Выполнение PATCH-запроса
# response = requests.put(f"{oncall_api_url}/{alert_id}", headers=headers, json=data)
response = requests.post(f"{oncall_api_url}", headers=headers)
print(response.status_code)
# print(response.json())
# Проверка статуса ответа
# if response.status_code == 200:
#     print("Alert status updated successfully.")
# else:
#     print(f"Failed to update alert status. Status code: {response.status_code}, Response: {response.text}")
