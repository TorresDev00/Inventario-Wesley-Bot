from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from mysql.connector import connect, Error
from DBConnect import DBConnect

class ActionCheckInventory(Action):

    def name(self) -> Text:
        return "action_check_inventory"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Obtener el nombre del medicamento y el id de la sede
        medicamento = next(tracker.get_latest_entity_values("medicamento"), None)
        print(f"Medicamento extraído: {medicamento}")

        id_sede = 1  # Ejemplo: cambia esto para obtener `id_sede` dinámicamente si es necesario
        
        if medicamento:
            # Instanciar el gestor de la base de datos
            db = DBConnect()

            # Consulta SQL
            query = """
                SELECT
                    ps.id_producto_sede as id,
                    ps.presentacion_producto,
                    ps.presentacion_peso,
                    ps.medida,
                    ps.lote,
                    ps.fecha_vencimiento,
                    ps.cantidad as inventario,
                    ps.tipo,
                    ps.clase,
                    ps.tipo_inventario
                FROM
                    vw_producto_sede_detallado ps
                WHERE
                    id_sede = %s
                    AND ps.cantidad > 0
                    AND ps.presentacion_producto LIKE %s
            """
            # Ejecutar consulta
            result = db.execute_query(query, (id_sede, f"%{medicamento}%"))

            if result:
                # Preparar una respuesta con los detalles del inventario
                respuesta = "Detalles del inventario para el medicamento solicitado:\n"
                for item in result:
                    respuesta += (f"- {item['presentacion_producto']} ({item['presentacion_peso']} {item['medida']}), "
                                  f"Lote: {item['lote']}, Vence: {item['fecha_vencimiento']}, "
                                  f"Cantidad disponible: {item['inventario']}\n")
                dispatcher.utter_message(text=respuesta)
            else:
                dispatcher.utter_message(
                    text=f"No tenemos {medicamento} disponible en inventario actualmente."
                )
        else:
            dispatcher.utter_message(
                text="Por favor, especifica el nombre del medicamento que deseas consultar."
            )

        return []
