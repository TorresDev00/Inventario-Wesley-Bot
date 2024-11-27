from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.DBConnect import DBConnect

class ActionCheckDateExpiry(Action): 
    def name(self) -> Text:
        return "action_check_date_expiry"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        medicamento = next(tracker.get_latest_entity_values("medicamento"), None)

        print(f"Medicamento extraído para consultar: {medicamento}")
        
        id_sede = 1
        
        if medicamento:
            db = DBConnect()
            
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
                AND id_sede = %s
                AND tp.nombrepro LIKE %s
                AND ps.fecha_vencimiento IS NOT NULL;
            """
            
            result = db.execute_query(query, (id_sede, f"%{medicamento}%"))
            print(f"Resultados encontrados: {result}")

            if result:
                vencidos = []
                por_vencerse = []
                
                for fila in result:
                    dias_restantes = fila["dias_restantes"]
                    if dias_restantes < 0:
                        vencidos.append(fila)
                    elif dias_restantes <= 30:  # Rango ajustable para "por vencerse"
                        por_vencerse.append(fila)
                
                mensaje = f"Resultados para el medicamento: {medicamento}:\n\n"
                
                if vencidos:
                    mensaje += "Lotes vencidos:\n"
                    for fila in vencidos:
                        mensaje += "- Producto: {} | Días vencidos: {} | Cantidad: {}\n".format(
                            fila["producto"],
                            abs(fila["dias_restantes"]),
                            fila["cantidad"]
                        )
                
                if por_vencerse:
                    mensaje += "\nLotes próximos a vencerse:\n"
                    for fila in por_vencerse:
                        mensaje += "- Producto: {} | Días restantes: {} | Cantidad: {}\n".format(
                            fila["producto"],
                            fila["dias_restantes"],
                            fila["cantidad"]
                        )
                
                if not vencidos and not por_vencerse:
                    mensaje = f"No se encontraron lotes vencidos ni próximos a vencerse para el medicamento {medicamento} en esta sede."
                
                dispatcher.utter_message(text=mensaje)
            else:
                dispatcher.utter_message(text=f"No se encontraron datos del medicamento {medicamento} en esta sede.")
        else:
            dispatcher.utter_message(text="No se pudo identificar el medicamento. Por favor, inténtalo de nuevo especificando el nombre del medicamento.")
        
        return []
