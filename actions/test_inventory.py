from mysql.connector import connect, Error

class ActionCheckInventory:
    def __init__(self, medicamento):
        self.medicamento = medicamento
        self.id_sede = 1  # Cambia el id de sede si es necesario

    def check_inventory(self):
        if self.medicamento:
            try:
                # Conexión a la base de datos
                connection = connect(
                    host="localhost",       # Cambia esto a tu host de la BD
                    user="root",            # Cambia esto a tu usuario de la BD
                    password="",            # Cambia esto a tu contraseña de la BD
                    database="wesley_inventario"  # Cambia esto a tu base de datos
                )
                
                cursor = connection.cursor(dictionary=True)
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
                cursor.execute(query, (self.id_sede, f"%{self.medicamento}%"))
                result = cursor.fetchall()

                if result:
                    respuesta = "Detalles del inventario para el medicamento solicitado:\n"
                    for item in result:
                        respuesta += (f"- {item['presentacion_producto']} ({item['presentacion_peso']} {item['medida']}), "
                                      f"Lote: {item['lote']}, Vence: {item['fecha_vencimiento']}, "
                                      f"Cantidad disponible: {item['inventario']}\n")
                    print(respuesta)
                else:
                    print(f"No tenemos {self.medicamento} disponible en inventario actualmente.")
            
            except Error as e:
                print(f"Error al conectar con la base de datos: {e}")
            
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            print("Por favor, especifica el nombre del medicamento que deseas consultar.")


# Llamada de prueba
medicamento = "Acetaminofén"  # Cambia esto al medicamento que quieres consultar
action = ActionCheckInventory(medicamento)
action.check_inventory() 
