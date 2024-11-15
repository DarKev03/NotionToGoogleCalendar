from notion import get_notion_tasks
from google_calendar import get_google_calendar_service, create_google_calendar_event, is_task_in_google_calendar

def sync_notion_with_google_calendar():
    tasks = get_notion_tasks()
    service = get_google_calendar_service()
    for task in tasks:
        if not is_task_in_google_calendar(service, task['name'], task['date']):
            create_google_calendar_event(service, task)

if __name__ == "__main__":
    sync_notion_with_google_calendar()
