# Notion Google Calendar Sync

Este proyecto sincroniza las tareas de una base de datos de Notion con Google Calendar.

## Configuración
- Crea una integración en Notion y agrega el token de integración en `config/config.py`.
- Habilita la Google Calendar API y descarga el archivo de credenciales `credentials.json`, colócalo en la carpeta `config/`.

## Instalación
```sh
git clone https://github.com/tu-usuario/notion-google-calendar-sync.git
cd notion-google-calendar-sync
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
