import mysql.connector

import os


def dbConnection():
    try:
        # Crear la conexión a la base de datos MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='181023040510',
            database='kuder'
        )
        return connection
    except mysql.connector.Error as err:
        print("Error de conexión a la base de datos MySQL:", err)
        return None
