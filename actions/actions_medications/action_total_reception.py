from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.DBConnect import DBConnect

class ActionTotalReception(Action):
    def name(self) -> Text:
        return "action_total_donaciones_recibidas_mes"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            db = DBConnect()

            id_sede = 1

            query = """ 
                SELECT 
                    presentacion_producto AS producto,
                    SUM(cantidad) AS total_donado,
                    tipo,
                    nombre_sede,
                    id_sede
                FROM 
                    vw_entrada_inventario ve
                WHERE 
                    tipo COLLATE utf8mb4_unicode_ci = 'Recepción nacional' COLLATE utf8mb4_unicode_ci AND
                    ve.id_sede = %s
                GROUP BY 
                    presentacion_producto, tipo, nombre_sede, id_sede
                ORDER BY 
                    total_donado DESC
                LIMIT 1;

            """
            
            result = db.execute_query(query,(id_sede,))

            if result:
                producto = result[0]['producto']
                total_donado = result[0]['total_donado']
                nombre_sede = result[0]['nombre_sede']

                message = (
                    f"\U0001F4E6 *Donación más recibida a través de Recepción Nacional:*\n"
                    f"Producto: {producto}\n"
                    f"Cantidad total: {total_donado} unidades\n"
                    f"Sede: {nombre_sede}."
                )
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="No se encontraron datos de donaciones nacionales.")

        except Exception as e:
            dispatcher.utter_message(text=f"Ocurrió un error al obtener los datos: {str(e)}")

        return []
