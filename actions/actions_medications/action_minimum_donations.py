from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.DBConnect import DBConnect

class ActionMinimunDonations(Action):
    def name(self) -> Text:
        return "action_minima_donacion"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        db = DBConnect()
        
        id_sede = 1
        
        query = """ 
        SELECT 
            COUNT(*) AS cantidad, 
            CONCAT(ps.lote, ': ', tp.nombrepro, ' ', pr.peso, ' ', m.nombre) AS producto 
        FROM donaciones don 
            INNER JOIN det_donacion det_don ON don.id_donaciones = det_don.id_donaciones 
            INNER JOIN producto_sede ps ON det_don.id_producto_sede = ps.id_producto_sede 
            INNER JOIN producto p ON ps.cod_producto = p.cod_producto
            INNER JOIN tipo_producto tp ON p.id_tipoprod = tp.id_tipoprod
            INNER JOIN presentacion pr ON pr.cod_pres = p.cod_pres
            INNER JOIN medida m ON m.id_medida = pr.id_medida
        WHERE
        ps.id_sede = %s
        GROUP BY ps.lote, tp.nombrepro, pr.peso, m.nombre, p.cod_producto
        ORDER BY cantidad ASC
        LIMIT 1;
        """
        try:
            # Ejecuta el query
            result = db.execute_query(query, (id_sede,))
            print(f"Resultados encontrados: {result}")
            
            if result:
                fila = result[0]
                mensaje = (
                    f"El medicamento menos donado es: {fila['producto']} "
                    f"con un total de {fila['cantidad']} donaciones registradas."
                )
            else:
                mensaje = "No se encontraron registros de donaciones en la base de datos."
        
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            mensaje = "Ocurrió un error al consultar el medicamento menos donado. Por favor, intenta más tarde."
        
        # Envía el mensaje al usuario
        dispatcher.utter_message(text=mensaje)
        return []