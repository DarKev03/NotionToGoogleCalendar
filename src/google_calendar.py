import os
import pickle
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build   
from google.auth.credentials import Credentials
from datetime import datetime, timedelta, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import SCOPES

# Conexión con Google Calendar usando OAuth
def get_google_calendar_service():
    creds = None

    # Verificar si existe el archivo de credenciales
    if not os.path.exists('config/credentials.json'):
        raise FileNotFoundError("The credentials.json file does not exist. Please ensure it is created correctly.")

    # Crear el flujo de autenticación desde el archivo de credenciales
    flow = InstalledAppFlow.from_client_secrets_file('config/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Guardar las credenciales para futuras ejecuciones
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


# Crear eventos en Google Calendar
def create_google_calendar_event(service, task):
    if "T" in task['date']:
        task['date'] = task['date'].split("T")[0] 

    # Crear el evento con los datos corregidos
    event = {
        'summary': task['name'],
        'start': {
            'date': task['date'],  
            'timeZone': 'UTC',
        },
        'end': {
            'date': task['date'],  
            'timeZone': 'UTC',
        },
    }
    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"Error creating event: {e}")

# Verificar si una tarea ya existe en Google Calendar
def is_task_in_google_calendar(service, task_name, task_date):
    try:
        # Convertir la fecha de la tarea a un objeto datetime
        task_date_dt = datetime.strptime(task_date, "%Y-%m-%d")

        # Definir los límites de tiempo para el día de la tarea
        time_min = (task_date_dt - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc).isoformat()
        time_max = (task_date_dt - timedelta(days=1)).replace(hour=23, minute=59, second=0, microsecond=0, tzinfo=timezone.utc).isoformat()

        # Hacer la solicitud a la API de Google Calendar
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
    except Exception as e:
        print(f"Error fetching events: {e}")
        return False

    events = events_result.get('items', [])
    for event in events:
        if event['summary'].strip().lower() == task_name.strip().lower():
            return True
    return False
