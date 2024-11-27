from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.DBConnect import DBConnect

class ActionMostEnteredMedication(Action):
    def name(self) -> Text:
      return "action_most_entered_medication"
  
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        db = DBConnect()
        
        query = """
        SELECT
            vi.presentacion_producto,
            SUM(vi.cantidad) AS total_entrada,
            vi.tipo,
            MONTH(vi.fecha) AS mes,
            vi.nombre_sede
        FROM
            vw_entrada_inventario vi
        WHERE
            YEAR(vi.fecha) = YEAR(CURRENT_DATE()) 
            AND MONTH(vi.fecha) = MONTH(CURRENT_DATE())
        GROUP BY
            vi.presentacion_producto,
            vi.tipo,
            MONTH(vi.fecha),
            vi.nombre_sede
        ORDER BY
            total_entrada DESC
        LIMIT 1;
        """
        
        result = db.execute_query(query)
        print(f"resultado encontrado {result}")
        
        if result:
            fila = result[0]
            mensaje = (
                f"El medicamento con mayor entrada este mes es: {fila['presentacion_producto']} "
                f"con un total de {fila['total_entrada']} unidades en la sede {fila['nombre_sede']}."
            )
        else: 
            mensaje = "No se encontraron datos de medicamentos con entradas este mes."
        
        dispatcher.utter_message(text=mensaje)
        
        return []