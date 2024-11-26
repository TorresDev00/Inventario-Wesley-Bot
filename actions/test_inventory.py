from actions.DBConnect import DBConnect

def test_db_connection():
    db = DBConnect()

    # Consulta de prueba (ajusta esto a una tabla válida en tu base de datos)
    query = "SELECT * FROM vw_producto_sede_detallado LIMIT 5"
    result = db.execute_query(query)

    if result:
        print("Conexión exitosa. Resultados obtenidos:")
        for row in result:
            print(row)
    else:
        print("Error al obtener datos o la consulta no devolvió resultados.")

if __name__ == "__main__":
    test_db_connection()
