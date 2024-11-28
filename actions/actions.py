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
        # log_action_usage(self.name())
        dispatcher.utter_message(text="Lo siento, no entendí tu pregunta.")
        return []