import mysql.connector

import os


def dbConnection():
    try:
        # Crear la conexión a la base de datos MySQL
        connection = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DATABASE')
        )
        return connection
    except mysql.connector.Error as err:
        print("Error de conexión a la base de datos MySQL:", err)
        return None
