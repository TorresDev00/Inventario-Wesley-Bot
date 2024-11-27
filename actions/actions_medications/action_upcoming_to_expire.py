from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.DBConnect import DBConnect

class ActionUpcomingProductsToExpire(Action):
    def name(self) -> Text:
        return "action_proximo_vencimiento"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        db = DBConnect()
        
        id_sede = 1
        
        query = """
            SELECT
                CONCAT(
                    ps.lote,
                    ': ',
                    tp.nombrepro,
                    ' ',
                    pr.peso,
                    ' ',
                    m.nombre
                ) AS producto,
                DATEDIFF(ps.fecha_vencimiento, NOW()) AS dias_restantes,
                ps.cantidad
            FROM
                producto_sede ps
            INNER JOIN producto p ON
                p.cod_producto = ps.cod_producto
            INNER JOIN tipo_producto tp ON
                tp.id_tipoprod = p.id_tipoprod
            INNER JOIN presentacion pr ON
                pr.cod_pres = p.cod_pres
            INNER JOIN medida m ON
                m.id_medida = pr.id_medida
            WHERE
                ps.cantidad > 0
                AND ps.id_sede = %s
                AND DATEDIFF(ps.fecha_vencimiento, NOW()) BETWEEN 0 AND 30
                AND ps.fecha_vencimiento IS NOT NULL;
        """
        
        try:
            result = db.execute_query(query, (id_sede,))
            print(f"Resultados encontrados: {result}")
            
            if result:
                # Construye el mensaje con los resultados
                mensajes = [
                    f"- {fila['producto']}: {fila['dias_restantes']} días restantes ({fila['cantidad']} unidades)."
                    for fila in result
                ]
                mensaje = "Los siguientes medicamentos están próximos a vencer en los próximos 30 días:\n" + "\n".join(mensajes)
            else:
                mensaje = "No se encontraron medicamentos próximos a vencer en los próximos 30 días."
        
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            mensaje = "Ocurrió un error al consultar los medicamentos próximos a vencer. Por favor, intenta más tarde."
        
        # Envía el mensaje al usuario
        dispatcher.utter_message(text=mensaje)
        return []