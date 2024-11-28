from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.DBConnect import DBConnect

class ActionTotalDonation(Action):
    def name(self) -> Text:
        return "action_total_donaciones_enviadas_mes"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            db = DBConnect()

            id_sede = 1  # O puedes obtenerlo de algún otro lugar, como una variable del tracker

            query = """ 
            SELECT SUM(cantidad) AS total_donaciones
            FROM vw_salida_inventario
            WHERE tipo COLLATE utf8mb4_unicode_ci = 'Donaciones' 
            AND id_sede = %s
            AND MONTH(fecha) = MONTH(CURRENT_DATE())
            AND YEAR(fecha) = YEAR(CURRENT_DATE());

            """
            
            result = db.execute_query(query, (id_sede,))

            total_donaciones = result[0]["total_donaciones"] if result and result[0]["total_donaciones"] is not None else 0

            dispatcher.utter_message(text=f"El total de donaciones entregadas este mes es: {total_donaciones}")
        
        except Exception as e:
            dispatcher.utter_message(text="Hubo un error al consultar el total de donaciones.")
            print(f"Error en la consulta: {e}")
        
        return []
