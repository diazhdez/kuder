from flask import Blueprint, render_template, url_for, redirect, flash, session, request

from functions.functions import get_admin

from datetime import datetime

from random import randint

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

import smtplib

import bcrypt

import os

import mysql.connector

import database.database as dbase

db = dbase.dbConnection()

admin_routes = Blueprint('admin', __name__)


# Ruta para el administrador
@admin_routes.route('/admin/')
def admin():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        admin = get_admin(email)
        if admin:
            return render_template('admin.html', admin=admin)
    else:
        return redirect(url_for('session.login'))


# Ruta de para registrar aspirantes y administradores
@admin_routes.route('/admin/registro/')
def registro():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        admin = get_admin(email)
        if admin:
            return render_template('registro.html')
    else:
        return redirect(url_for('session.login'))


# Ruta para registrar a los usuarios
@admin_routes.route('/register_user/', methods=['POST', 'GET'])
def register_user():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        admin = get_admin(email)
        if admin:
            if request.method == 'POST':
                try:
                    # Obtener la cantidad de usuarios a registrar desde el formulario
                    num_users = int(request.form['num_users'])
                    # Contraseña predeterminada para todos los usuarios
                    password = request.form['password']

                    cursor = db.cursor()

                    # Generar los documentos de los usuarios
                    user_docs = []
                    for _ in range(num_users):
                        email = str(randint(100000, 999999))
                        hashpass = bcrypt.hashpw(
                            password.encode('utf-8'), bcrypt.gensalt())
                        # Obtener la fecha y hora actual
                        date = datetime.now()
                        user_docs.append((email, hashpass, date))

                    # Insertar los documentos de los usuarios en la base de datos
                    cursor.executemany(
                        "INSERT INTO user (email, password, date) VALUES (%s, %s, %s)", user_docs)
                    db.commit()

                    flash(f'Se registraron {num_users} usuarios correctamente')
                    return redirect(url_for('admin.registro'))
                except mysql.connector.Error as err:
                    print("Error al registrar usuarios:", err)
                    db.rollback()
                finally:
                    cursor.close()
        else:
            return redirect(url_for('session.login'))

    return redirect(url_for('admin.registro'))


# Ruta para registrar administradores
@admin_routes.route('/register_admin/', methods=['POST', 'GET'])
def register_admin():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        admin = get_admin(email)
        if admin:
            if request.method == 'POST':
                cursor = db.cursor()
                try:
                    existing_admin = request.form['email']
                    name = request.form['name']
                    email = request.form['email']
                    password = request.form['password']
                    phone = request.form['phone']

                    # Verificar si el administrador ya existe en la base de datos
                    cursor.execute(
                        "SELECT * FROM admin WHERE email = %s", (email,))
                    existing_admin = cursor.fetchone()

                    if existing_admin is None:
                        # Hash de la contraseña
                        hashpass = bcrypt.hashpw(
                            password.encode('utf-8'), bcrypt.gensalt())

                        # Insertar el nuevo administrador en la base de datos
                        cursor.execute(
                            "INSERT INTO admin (name, email, password, phone) VALUES (%s, %s, %s, %s)", (name, email, hashpass, phone))
                        db.commit()

                        flash('Se registró el administrador correctamente')
                        return redirect(url_for('admin.registro'))
                    else:
                        flash('El correo ya está en uso')
                        return redirect(url_for('admin.registro'))
                except mysql.connector.Error as err:
                    print("Error al registrar administrador:", err)
                    db.rollback()
                finally:
                    cursor.close()
        else:
            return redirect(url_for('session.login'))

    return redirect(url_for('admin.registro'))


# Ruta para visualizar los aspirantes
@admin_routes.route('/admin/listas/users/', methods=['POST', 'GET'])
def users():
    if 'email' in session:
        email = session['email']
        admin = get_admin(email)
        if admin:
            if request.method == 'POST':
                search_query = request.form.get('search_query')
                cursor = db.cursor(dictionary=True)
                try:
                    # Consulta para buscar usuarios por nombre, email o carrera
                    query = "SELECT * FROM user WHERE name LIKE %s OR email LIKE %s OR carrera LIKE %s"
                    cursor.execute(query, ('%' + search_query + '%',
                                   '%' + search_query + '%', '%' + search_query + '%'))
                    users = cursor.fetchall()
                    return render_template('users.html', users=users)
                except mysql.connector.Error as err:
                    print("Error al buscar usuarios:", err)
                finally:
                    cursor.close()
            else:
                cursor = db.cursor(dictionary=True)
                try:
                    # Consulta para obtener todos los usuarios
                    cursor.execute("SELECT * FROM user")
                    users = cursor.fetchall()
                    return render_template('users.html', users=users)
                except mysql.connector.Error as err:
                    print("Error al obtener usuarios:", err)
                finally:
                    cursor.close()
        else:
            return redirect(url_for('session.login'))
    else:
        return redirect(url_for('session.login'))


# Ruta para eliminar un aspirante
@admin_routes.route('/delete/<int:user_id>/')
def delete_user(user_id):
    cursor = db.cursor()
    try:
        # Consulta para eliminar el aspirante por ID
        cursor.execute("DELETE FROM user WHERE id = %s", (user_id,))
        db.commit()
    except mysql.connector.Error as err:
        print("Error al eliminar usuario:", err)
        db.rollback()
    finally:
        cursor.close()
    return redirect(url_for('admin.users'))


# Ruta para visualizar los administradores
@admin_routes.route('/admin/listas/admins/')
def admins():
    if 'email' in session:
        email = session['email']
        admin = get_admin(email)
        if admin:
            cursor = db.cursor(dictionary=True)
            try:
                # Consulta para obtener todos los administradores
                cursor.execute("SELECT * FROM admin")
                admins = cursor.fetchall()
                return render_template('admins.html', admins=admins)
            except mysql.connector.Error as err:
                print("Error al obtener administradores:", err)
            finally:
                cursor.close()
        else:
            return redirect(url_for('session.login'))
    else:
        return redirect(url_for('session.login'))


# Ruta para eliminar un administrador
@admin_routes.route('/delete/<int:admin_id>/')
def delete_admin(admin_id):
    cursor = db.cursor()
    try:
        # Consulta para eliminar el administrador por ID
        cursor.execute("DELETE FROM admin WHERE id = %s", (admin_id,))
        db.commit()
    except mysql.connector.Error as err:
        print("Error al eliminar administrador:", err)
        db.rollback()
    finally:
        cursor.close()
    return redirect(url_for('admin.admins'))


# Ruta para visualizar los correos
@admin_routes.route('/admin/correos/')
def correos():
    if 'email' in session:
        email = session['email']
        admin = get_admin(email)
        if admin:
            cursor = db.cursor(dictionary=True)
            try:
                # Consulta para obtener todos los correos
                cursor.execute("SELECT * FROM email")
                correos = cursor.fetchall()
                return render_template('email.html', correos=correos)
            except mysql.connector.Error as err:
                print("Error al obtener correos:", err)
            finally:
                cursor.close()
        else:
            return redirect(url_for('session.login'))
    else:
        return redirect(url_for('session.login'))


# Función para enviar correo a empleados aceptados
def enviar_mensaje_aceptado(empleado):
    email = 'contact.quarium@gmail.com'
    password = 'otjt nkts nczg qcxw'
    destinatario = empleado['correo']

    template_file = os.path.join('templates', 'correo_aceptacion.html')

    # Cargar el contenido del archivo HTML
    with open(template_file, 'r') as file:
        html_content = file.read()

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = email
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Registro Aceptado'

    # Adjuntar el contenido HTML al mensaje
    mensaje.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        texto_del_correo = mensaje.as_string()
        server.sendmail(email, destinatario, texto_del_correo)
        server.quit()
        print('Correo enviado correctamente a', destinatario)
    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')
