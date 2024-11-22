import os
import pickle
import sys
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build   
from google.auth.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import SCOPES
from datetime import datetime, timedelta, timezone


# Conexión con Google Calendar
def get_google_calendar_service():
    creds = None
    token_file = 'token.pickle'
    
    # Cargar credenciales desde el archivo token.pickle si existe
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # Si las credenciales no son válidas, refrescarlas o generar nuevas
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Cargar las credenciales desde la variable de entorno
            credentials_json = os.getenv("GOOGLE_CREDENTIALS")
            if not credentials_json:
                raise ValueError("La variable de entorno GOOGLE_CREDENTIALS no está configurada.")
            
            credentials_info = json.loads(credentials_json)
            creds = ServiceAccountCredentials.from_service_account_info(credentials_info, scopes=SCOPES)
        
        # Guardar las credenciales actualizadas en token.pickle
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('calendar', 'v3', credentials=creds)
    return service

# Crear eventos en Google Calendar
def create_google_calendar_event(service, task):
    # Si la fecha contiene una "T", significa que tiene fecha y hora juntas; ajusta esto
    if "T" in task['date']:
        task['date'] = task['date'].split("T")[0]

    # Crear el evento con los datos corregidos
    event = {
        'summary': task['name'],
        'start': {
            'date': task['date'],  # Aquí usamos 'date' para eventos de día completo
            'timeZone': 'UTC',
        },
        'end': {
            'date': task['date'],  # Aquí usamos 'date' para eventos de día completo
            'timeZone': 'UTC',
        },
    }

    # Depuración: imprime los datos del evento antes de enviarlo
    print(f"Event data: {event}")

    try:
        # Crear el evento en Google Calendar
        event_result = service.events().insert(calendarId='primary', body=event).execute()

        # Depuración: confirma si el evento fue creado correctamente
        print(f"Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        # Capturar y mostrar cualquier error durante la creación del evento
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

def list_calendars(service):
    calendars = service.calendarList().list().execute()
    for calendar in calendars['items']:
        print(f"ID: {calendar['id']}, Name: {calendar['summary']}")
