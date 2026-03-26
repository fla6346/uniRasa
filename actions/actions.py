from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import os

# URL de tu backend Node.js en cPanel
BACKEND_URL = os.environ.get("BACKEND_URL", "https://https://cidtec-uc.com/api")

class ActionConsultarEventos(Action):
    def name(self) -> Text:
        return "action_consultar_eventos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            response = requests.get(f"{BACKEND_URL}/eventos", timeout=8)
            eventos = response.json()

            if not eventos or len(eventos) == 0:
                dispatcher.utter_message(text="No hay eventos próximos por el momento.")
                return []

            mensaje = "📅 *Próximos eventos:*\n"
            for e in eventos[:5]:  # máximo 5
                mensaje += f"\n• *{e.get('nombre', 'Sin nombre')}*"
                mensaje += f"\n  📆 {e.get('fecha', 'Fecha no definida')}"
                mensaje += f"\n  🕐 {e.get('hora', 'Hora no definida')}"
                mensaje += f"\n  📍 {e.get('lugar', 'Lugar no definido')}\n"

            dispatcher.utter_message(text=mensaje)
        except Exception as e:
            dispatcher.utter_message(text="No pude obtener los eventos en este momento.")
        return []


class ActionGuardarEvento(Action):
    def name(self) -> Text:
        return "action_guardar_evento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre = tracker.get_slot("nombre_evento")
        fecha  = tracker.get_slot("fecha")
        hora   = tracker.get_slot("hora")
        lugar  = tracker.get_slot("lugar")

        try:
            response = requests.post(f"{BACKEND_URL}/eventos", json={
                "nombre": nombre,
                "fecha": fecha,
                "hora": hora,
                "lugar": lugar,
            }, timeout=8)

            if response.status_code == 201:
                dispatcher.utter_message(
                    text=f"✅ Evento *{nombre}* creado para el {fecha} a las {hora} en {lugar}."
                )
            else:
                dispatcher.utter_message(text="No pude guardar el evento. Intenta más tarde.")
        except Exception as e:
            dispatcher.utter_message(text="Error al guardar el evento.")
        return []


class ActionNoPermisoCrearEvento(Action):
    def name(self) -> Text:
        return "action_no_permiso_crear_evento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Lo siento, no tienes permiso para crear eventos."
        )
        return []