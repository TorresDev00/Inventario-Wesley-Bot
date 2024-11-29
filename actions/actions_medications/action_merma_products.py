from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.DBConnect import DBConnect

class ActionMermaProducts(Action):
    def name(self) -> Text:
        return "action_medicamentos_perdidos"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        db = DBConnect()
        
        id_sede = 1
        
        query = """
        SELECT
            CONCAT(ps.lote, ': ', tp.nombrepro, ' ', pr.peso, ' ', m.nombre) AS producto,
            SUM(dd.cantidad) AS cantidad_perdida
        FROM
            descargo d
        INNER JOIN detalle_descargo dd ON
            dd.id_descargo = d.id_descargo
        INNER JOIN producto_sede ps ON
            ps.id_producto_sede = dd.id_producto_sede
        INNER JOIN producto p ON
            ps.cod_producto = p.cod_producto
        INNER JOIN tipo_producto tp ON
            p.id_tipoprod = tp.id_tipoprod
        INNER JOIN presentacion pr ON
            pr.cod_pres = p.cod_pres
        INNER JOIN medida m ON
            m.id_medida = pr.id_medida
        WHERE
            d.fecha >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
            AND ps.id_sede = %s
        GROUP BY
            ps.lote, tp.nombrepro, pr.peso, m.nombre
        ORDER BY
            cantidad_perdida DESC
        LIMIT 5;
        """
        
        try:
            # Ejecutar la consulta
            results = db.execute_query(query, (id_sede,))
            print(f"Resultados encontrados: {results}")
            
            if results:
                mensaje = ":b:Los productos con más pérdidas en el último mes son: :/b: \n"
                for i,fila in enumerate(results):
                    mensaje += (
                        f"{i+1}.- {fila['producto']} con un total de {fila['cantidad_perdida']} unidades perdidas.\n"
                    )
            else:
                mensaje = "No se encontraron registros de pérdidas en el último mes."
        
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            mensaje = "Ocurrió un error al consultar los productos con más pérdidas. Por favor, intenta más tarde."
        
        # Enviar el mensaje al usuario
        dispatcher.utter_message(text=mensaje)
        return []
