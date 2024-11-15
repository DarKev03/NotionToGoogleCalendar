import requests
from config.config import NOTION_TOKEN, DATABASE_ID

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
            task_name = properties["Name"]["title"][0]["text"]["content"]
            task_date = properties.get("Date", {}).get("date", {}).get("start")
            if task_date:
                tasks.append({"name": task_name, "date": task_date})
        return tasks
    else:
        print(f"Error fetching Notion tasks: {response.status_code}")
        return []
