# actions/actions.py

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# 🔥 Usa tu IP local, NO localhost
BACKEND_URL = "http://192.168.0.167:3001"  # ⚠️ ¡Cambia esto por tu IP real!

class ActionConsultarEventos(Action):
    def name(self) -> Text:
        return "action_consultar_eventos"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            response = requests.get(f"{BACKEND_URL}/api/eventos", timeout=5)
            response.raise_for_status()
            eventos = response.json()

            if not eventos:
                dispatcher.utter_message(text="Por el momento no hay eventos programados.")
                return []

            lista_formateada = "\n".join([
                f"- {evento.get('nombreevento', 'Evento sin nombre')} "
                f"(Fecha: {evento.get('fechaevento', 'N/A')})"
                for evento in eventos
            ])
            
            mensaje_final = f"Claro, aquí tienes los próximos eventos:\n{lista_formateada}"
            dispatcher.utter_message(text=mensaje_final)

        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API de eventos: {e}")
            dispatcher.utter_message(text="Lo siento, tuve un problema al consultar los eventos. Por favor, intenta de nuevo más tarde.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            dispatcher.utter_message(text="Lo siento, ocurrió un error inesperado.")

        return []

class ActionNoPermisoCrearEvento(Action):  # 👈 Nombre más claro
    def name(self) -> Text:
        return "action_no_permiso_crear_evento"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Mensaje claro + redirección
        dispatcher.utter_message(
            text="Lo siento, solo los usuarios académicos pueden crear eventos. "
                 "Si eres académico, por favor inicia sesión con tu cuenta correspondiente.",
            custom={
                "type": "navigate",
                "payload": {
                    "route": "/admin/Login"  # Asegúrate de que esta ruta exista en tu Expo Router
                }
            }
        )
        return []

class ActionVincularCuenta(Action):
    def name(self) -> Text:
        return "action_vincular_cuenta"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chat_id = tracker.sender_id
        email = next(tracker.get_latest_entity_values("email"), None)

        if not email:
            dispatcher.utter_message(text="No entendí tu email. Por favor, di algo como 'vincular mi cuenta con usuario@email.com'")
            return []

        try:
            response = requests.post(
                f"{BACKEND_URL}/api/users/link-telegram",
                json={"email": email, "chat_id": chat_id},
                timeout=5
            )
            response.raise_for_status()
            dispatcher.utter_message(text="¡Genial! Tu cuenta ha sido vinculada. Ahora recibirás notificaciones por aquí.")
        except requests.exceptions.RequestException:
            dispatcher.utter_message(text="Lo siento, no pude vincular tu cuenta. Asegúrate de que el email sea correcto.")
        
        return []