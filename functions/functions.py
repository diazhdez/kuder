from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

import smtplib

import os

import mysql.connector

import database.database as dbase

# Obtener la conexión a la base de datos
db = dbase.dbConnection()


# Función para obtener un usuario por su correo electrónico
def get_user(email):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print("Error al obtener usuario:", err)
    finally:
        cursor.close()


# Función para obtener un administrador por su correo electrónico
def get_admin(email):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
        admin = cursor.fetchone()
        return admin
    except mysql.connector.Error as err:
        print("Error al obtener administrador:", err)
    finally:
        cursor.close()


# Función para verificar si el usuario ha completado el test
def user_has_completed_survey(user_id):
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM answers WHERE user_id = %s", (str(user_id),))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print("Error al verificar si el usuario ha completado el test:", err)
    finally:
        cursor.close()


# Función para verificar si el usuario ha completado el formulario de HubSpot
def user_has_completed_hubspot_form(user_id):
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM hubspot WHERE user_id = %s", (str(user_id),))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(
            "Error al verificar si el usuario ha completado el formulario de HubSpot:", err)
    finally:
        cursor.close()


# Función para enviar correos
def enviar_correo_contacto(name, subject, message):
    # Correo desde el que se enviarán los mensajes
    email = os.environ.get('EMAIL')
    # Contraseña del correo
    password = os.environ.get('PASSWORD')

    # Correo que recibirá los mensajes de contacto
    destinatario = os.environ.get('DESTINATARIO')

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = email
    mensaje['To'] = destinatario
    # Utiliza el asunto proporcionado por el usuario
    mensaje['Subject'] = subject

    # Construye el contenido del mensaje con los datos proporcionados por el usuario
    contenido_mensaje = f"Nombre: {name}\nMensaje: {message}"

    # Adjuntar el contenido al mensaje
    mensaje.attach(MIMEText(contenido_mensaje))

    try:
        # Establecer conexión con el servidor SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)

        # Enviar el correo electrónico
        texto_del_correo = mensaje.as_string()
        server.sendmail(email, destinatario, texto_del_correo)
        server.quit()

        print('Correo enviado correctamente a', destinatario)
        return True  # Indica que el correo se envió correctamente
    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')
        return False  # Indica que hubo un error al enviar el correo
