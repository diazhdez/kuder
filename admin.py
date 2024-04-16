from flask import Blueprint, render_template, url_for, redirect, flash, session, request

import bcrypt

from bson import ObjectId

import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

import os

from functions import get_admin

import database as dbase

db = dbase.dbConnection()

admin_routes = Blueprint('admin', __name__)


# Ruta para el administrador
@admin_routes.route('/admin/')
def admin():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        admin = get_admin(email)
        if admin:
            return render_template('admin.html')
    else:
        return redirect(url_for('session.login'))


# Ruta de para registrar aspirantes y administradores
@admin_routes.route('/admin/registro/')
def registro():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
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
        # Función para obtener datos del usuario desde MongoDB
        admin = get_admin(email)
        if admin:
            if request.method == 'POST':
                users = db['users']
                existing_user = users.find_one(
                    {'email': request.form['email']})
                nombre = request.form['nombre']
                email = request.form['email']
                password = request.form['password']
                genero = request.form['genero']
                fecha = request.form['fecha']
                telefono = request.form['telefono']
                carrera = request.form['carrera']

                if existing_user is None:
                    hashpass = bcrypt.hashpw(
                        password.encode('utf-8'), bcrypt.gensalt())
                    users.insert_one({
                        'nombre': nombre,
                        'email': email,
                        'password': hashpass,
                        'genero': genero,
                        'fecha': fecha,
                        'telefono': telefono,
                        'carrera': carrera
                    })
                    return redirect(url_for('admin.registro'))

                flash('El correo ya está en uso')
                return redirect(url_for('admin.registro'))
        else:
            return redirect(url_for('session.login'))

    return redirect(url_for('admin.registro'))


# Ruta para registrar administradores
@admin_routes.route('/register_admin/', methods=['POST', 'GET'])
def register_admin():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        admin = get_admin(email)
        if admin:
            if request.method == 'POST':
                admin = db['admin']
                existing_admin = admin.find_one(
                    {'email': request.form['email']})
                nombre = request.form['nombre']
                email = request.form['email']
                password = request.form['password']
                area = request.form['area']
                genero = request.form['genero']
                fecha = request.form['fecha']
                telefono = request.form['telefono']

                if existing_admin is None:
                    hashpass = bcrypt.hashpw(
                        password.encode('utf-8'), bcrypt.gensalt())
                    admin.insert_one({
                        'nombre': nombre,
                        'email': email,
                        'password': hashpass,
                        'area': area,
                        'genero': genero,
                        'fecha': fecha,
                        'telefono': telefono
                    })
                    return redirect(url_for('admin.registro'))

                flash('El correo ya está en uso')
                return redirect(url_for('admin.registro'))
        else:
            return redirect(url_for('session.login'))

    return redirect(url_for('admin.registro'))


# Ruta para visualizar los aspirantes
@admin_routes.route('/admin/users/')
def users():
    if 'email' in session:
        email = session['email']
        admin = get_admin(email)
        if admin:
            users = db['users'].find()
            return render_template('users.html', users=users)
        else:
            return redirect(url_for('session.login'))
    else:
        return redirect(url_for('session.login'))


# Method DELETE
@admin_routes.route('/delete/<string:user_id>/')
def delete_user(user_id):
    users = db['users']
    users.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('admin.users'))


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
