import os
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

#Conexión a la API de Notion
def get_notion_tasks():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        tasks = []
        for result in data["results"]:
            properties = result["properties"]
            if properties.get("Tareas") and properties["Tareas"]["title"]:
                task_name = properties["Tareas"]["title"][0]["text"]["content"]
            try:
                task_date = properties.get("Fecha", {}).get("date", {}).get("start")
            except AttributeError:
                task_date = None
            if task_date:
                tasks.append({"name": task_name, "date": task_date})
        return tasks
    else:
        print(f"Error fetching Notion tasks: {response.status_code}{response.text}")
        return []

