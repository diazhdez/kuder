from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

import smtplib

import database.database as dbase

db = dbase.dbConnection()


def get_user(email):
    user = db['users'].find_one({'email': email})
    return user


def get_admin(email):
    admin = db['admin'].find_one({'email': email})
    return admin


# Función para verificar si el usuario ha completado el cuestionario
def user_has_completed_survey(user_id):
    respuestas = db['respuestas']
    return respuestas.find_one({'user_id': str(user_id)}) is not None


# Función para enviar correos
def enviar_correo_contacto(name, subject, message):
    # Correo desde el que se enviarán los mensajes
    email = 'contact.quarium@gmail.com'
    # Contraseña del correo
    password = 'otjt nkts nczg qcxw'

    # Correo que recibirá los mensajes de contacto
    destinatario = 'natividadv617@gmail.com'

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
