import os

# Configuración inicial para Notion y Google Calendar
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Validación para asegurar que las variables están configuradas
if not NOTION_TOKEN:
    raise ValueError("La variable de entorno NOTION_TOKEN no está configurada.")
if not DATABASE_ID:
    raise ValueError("La variable de entorno DATABASE_ID no está configurada.")
