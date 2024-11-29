import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Importar acciones desde otras subcarpetas
from actions.actions_medications.action_check_inventory import ActionCheckInventory
from actions.actions_medications.action_inventary_entry_month import ActionMostEnteredMedication
from actions.actions_medications.action_date_expiry import ActionCheckDateExpiry
from actions.actions_medications.test_inventory import test_db_connection
from actions.actions_medications.action_maxima_donacion import ActionMaximaDonacion
from actions.actions_medications.action_upcoming_to_expire import ActionUpcomingProductsToExpire
from actions.actions_medications.action_minimum_donations import ActionMinimunDonations
from actions.actions_medications.action_merma_products import ActionMermaProducts
from actions.actions_medications.action_maximum_sale import ActionMaximumSale
from actions.actions_medications.action_minimum_sale import ActionMinimumSale
from actions.actions_medications.action_total_reception import ActionTotalReception 
from actions.actions_medications.action_total_donation import ActionTotalDonation

# from actions.helpers.utils import log_action_usage

# Ejemplo de una acción base
class ActionDefault(Action):
    def name(self) -> Text:
        return "action_default_response"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Mensajes de respuesta cuando no se entiende la pregunta
        default_responses = [
            "Lo siento, no entendí tu pregunta. ¿Podrías reformularla?",
            "No estoy seguro de cómo responder eso. Intenta con algo más específico.",
            "Disculpa, no tengo una respuesta para eso. ¿Hay algo más en lo que pueda ayudarte?",
            "Esa pregunta me toma por sorpresa. Tal vez pueda ayudarte de otra manera."
        ]
        
        # Elegir un mensaje aleatorio
        response = random.choice(default_responses)
        
        # Opcional: Log de la interacción no entendida
        user_message = tracker.latest_message.get("text", "No se pudo capturar el texto.")
        print(f"Mensaje no entendido: {user_message}")
        
        # Opcional: Sugerencias para el usuario
        suggestions = [
            "Puedes intentar preguntar: '¿Cuántos medicamentos se vencen pronto?'",
            "Prueba con: '¿Cuántas donaciones se han recibido este mes?'",
            "Intenta: '¿Cuál es el medicamento más vendido?'"
        ]
        response += "\n\n" + random.choice(suggestions)
        
        # Enviar mensaje al usuario
        dispatcher.utter_message(text=response)
        
        return []