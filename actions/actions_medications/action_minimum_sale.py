from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.DBConnect import DBConnect

class ActionMinimumSale(Action):
    def name(self) -> Text:
        return "action_minima_venta"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            con = DBConnect()
            
            id_sede = 1
            
            query = """ 
            SELECT 
                CONCAT(ps.lote, ': ', tp.nombrepro, ' ', pr.peso, ' ', m.nombre) AS producto,
                SUM(vp.cantidad) AS total_vendido
            FROM
                venta v
            INNER JOIN venta_producto vp ON
                vp.num_fact = v.num_fact
            INNER JOIN producto_sede ps ON
                ps.id_producto_sede = vp.id_producto_sede
            INNER JOIN producto p ON
                ps.cod_producto = p.cod_producto
            INNER JOIN tipo_producto tp ON
                p.id_tipoprod = tp.id_tipoprod
            INNER JOIN presentacion pr ON
                pr.cod_pres = p.cod_pres
            INNER JOIN medida m ON
                m.id_medida = pr.id_medida
            WHERE
                ps.id_sede = %s
            GROUP BY 
                ps.lote, tp.nombrepro, pr.peso, m.nombre
            ORDER BY 
                total_vendido ASC
            LIMIT 1;
            """
            
            result = con.execute_query(query, (id_sede,))

            if result:
                producto = result[0]['producto']
                total_vendido = result[0]['total_vendido']
                message = (
                    f"\U0001F9EA *Medicamento menos vendido:*\n"
                    f"Nombre: {producto}\n"
                    f"Cantidad total vendida: {total_vendido} unidades."
                )
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="No se encontraron datos sobre el medicamento menos vendido.")

        except Exception as e:
            dispatcher.utter_message(text=f"Ocurrió un error al obtener los datos: {str(e)}")

        return []
