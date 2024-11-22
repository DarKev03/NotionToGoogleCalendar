from threading import Thread, Timer
from flask import Flask, jsonify, request
from google_calendar import create_google_calendar_event, get_google_calendar_service, is_task_in_google_calendar
from notion import get_notion_tasks


app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API funcionando correctamente"}), 200

@app.route("/sync", methods=["GET"])
def sync():
    try:
        # Sincronizar Notion con Google Calendar
        tasks = get_notion_tasks()
        service = get_google_calendar_service()

        for task in tasks:
            if not is_task_in_google_calendar(service, task['name'], task['date']):
                create_google_calendar_event(service, task)

        return jsonify({"message": "Sincronización completada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def periodic_sync():
    """Función que ejecuta la sincronización periódica."""
    print("Iniciando sincronización automática...")
    try:
        tasks = get_notion_tasks()
        service = get_google_calendar_service()

        for task in tasks:
            if not is_task_in_google_calendar(service, task['name'], task['date']):
                create_google_calendar_event(service, task)

        print("Sincronización automática completada.")
    except Exception as e:
        print(f"Error en la sincronización automática: {e}")

    # Programar la próxima ejecución
    Timer(60 * 60 * 5, periodic_sync).start()  # 5 horas

if __name__ == "__main__":
    # Inicia la sincronización automática en un hilo separado
    Thread(target=periodic_sync, daemon=True).start()
    app.run(debug=True)
