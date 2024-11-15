import os
import pickle
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build   
from google.auth.credentials import Credentials
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import SCOPES


#Conexión con Google Calendar
def get_google_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('calendar', 'v3', credentials=creds)
    return service

# Crear eventos en Google Calendar
def create_google_calendar_event(service, task):
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
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event_result.get('htmlLink')}")

# Verificar si una tarea ya existe en Google Calendar
def is_task_in_google_calendar(service, task_name, task_date):
    time_min = f"{task_date}T00:00:00Z"
    time_max = f"{task_date}T23:59:59Z"
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    for event in events:
        if event['summary'] == task_name:
            return True
    return False
