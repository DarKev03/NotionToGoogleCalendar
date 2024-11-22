from google_calendar import create_google_calendar_event, get_google_calendar_service, is_task_in_google_calendar
from notion import get_notion_tasks

# Sincronizar tareas de Notion con Google Calendar
def sync_notion_with_google_calendar():
    """
    Función principal que sincroniza las tareas de Notion con Google Calendar.
    """
    tasks = get_notion_tasks()
    service = get_google_calendar_service()
    for task in tasks:
        if not is_task_in_google_calendar(service, task['name'], task['date']):
            create_google_calendar_event(service, task)

# Handler para Vercel
def handler(request):
    """
    Handler compatible con Vercel. 
    Ejecuta la sincronización y devuelve un mensaje de confirmación.
    """
    try:
        sync_notion_with_google_calendar()
        return {
            "statusCode": 200,
            "body": "Sincronización completada correctamente"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error al sincronizar: {str(e)}"
        }

if __name__ == "__main__":
    sync_notion_with_google_calendar()
