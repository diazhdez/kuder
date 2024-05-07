from flask import Blueprint, render_template, url_for, redirect, flash, session, request, send_file

from functions.functions import get_admin

from functions.functions import get_user

from datetime import datetime

from random import randint

from bson import ObjectId

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

import smtplib

import bcrypt

import os

import database.database as dbase

from functools import wraps

import plotly.graph_objs as go


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
            return render_template('admin.html', admin=admin)
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
                # Obtener la cantidad de usuarios a registrar desde el formulario
                num_users = int(request.form['num_users'])
                # Contraseña predeterminada para todos los usuarios
                password = request.form['password']

                users = db['users']

                # Generar los documentos de los usuarios
                user_docs = []
                for _ in range(num_users):
                    email = str(randint(100000, 999999))
                    hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    # Obtener la fecha y hora actual
                    date = datetime.now()
                    user_docs.append({
                        'email': email,
                        'password': hashpass,
                        'datetime': date
                    })

                # Insertar los documentos de los usuarios en la base de datos
                users.insert_many(user_docs)

                flash(f'Se registraron {num_users} usuarios correctamente')
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
                name = request.form['name']
                email = request.form['email']
                password = request.form['password']
                phone = request.form['phone']

                if existing_admin is None:
                    hashpass = bcrypt.hashpw(
                        password.encode('utf-8'), bcrypt.gensalt())
                    admin.insert_one({
                        'name': name,
                        'email': email,
                        'password': hashpass,
                        'phone': phone
                    })
                    flash('Se registró el administrador correctamente')
                    return redirect(url_for('admin.registro'))

                flash('El correo ya está en uso')
                return redirect(url_for('admin.registro'))
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
                users = db['users'].find({
                    '$or': [
                        {'name': {'$regex': search_query, '$options': 'i'}},
                        {'email': {'$regex': search_query, '$options': 'i'}},
                        {'carrera': {'$regex': search_query, '$options': 'i'}}
                    ]
                })
            else:
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


# Ruta para visualizar los administradores
@admin_routes.route('/admin/listas/admins/')
def admins():
    if 'email' in session:
        email = session['email']
        admin = get_admin(email)
        if admin:
            admins = db['admin'].find()
            return render_template('admins.html', admins=admins)
        else:
            return redirect(url_for('session.login'))
    else:
        return redirect(url_for('session.login'))
    

# Method DELETE
@admin_routes.route('/delete/<string:admin_id>/')
def delete_admin(admin_id):
    admin = db['admin']
    admin.delete_one({'_id': ObjectId(admin_id)})
    return redirect(url_for('admin.admins'))


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


# Ruta para visualizar los correos
@admin_routes.route('/admin/correos/')
def correos():
    if 'email' in session:
        email = session['email']
        admin = get_admin(email)
        if admin:
            correos = db['correos'].find()
            return render_template('email.html', correos=correos)
        else:
            return redirect(url_for('session.login'))
    else:
        return redirect(url_for('session.login'))


# Ruta para que los administradores vean y descarguen la gráfica de todos los usuarios
@admin_routes.route('/admin/results/graph')
def admin_results_graph():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        admin = get_admin(email)
        if admin:
            # Obtener los datos de todos los usuarios desde MongoDB
            usuarios = db['users'].find()

            # Inicializar el contador de carreras para todos los usuarios
            carreras_count_total = {'TICS': 0,
                                    'Gastronomía': 0,
                                    'Mantenimiento Industrial': 0,
                                    'Desarrollo de Negocios': 0}

            # Iterar sobre todos los usuarios para recopilar datos
            for usuario in usuarios:
                carrera_usuario = usuario.get('carrera', 'Carrera no especificada')
                respuestas_usuario = db.respuestas.find({'user_id': str(usuario['_id'])})

                # Iterar sobre todas las respuestas del usuario
                for respuesta in respuestas_usuario:
                    # Iterar sobre las preguntas en cada respuesta
                    for pregunta, carrera in respuesta.items():
                        # Verificar si la respuesta corresponde a una carrera
                        if pregunta.startswith('pregunta_') and carrera in carreras_count_total:
                            # Incrementar el contador de la carrera correspondiente
                            carreras_count_total[carrera] += 1

            # Crear el gráfico de barras con Plotly para todos los usuarios
            data_total = [go.Bar(x=list(carreras_count_total.keys()),
                                 y=list(carreras_count_total.values()))]

            # Configurar el diseño del gráfico para todos los usuarios
            layout_total = go.Layout(title='Carreras de todos los usuarios',
                                     xaxis=dict(title='Carreras'),
                                     yaxis=dict(title='Número de respuestas'))

            # Crear la figura para todos los usuarios
            fig_total = go.Figure(data=data_total, layout=layout_total)

            # Convertir la figura a HTML
            graph_html_total = fig_total.to_html(full_html=False, include_plotlyjs='cdn')

            # Guardar la gráfica como archivo temporal
            graph_temp_file = "/tmp/graph_all_users.html"
            fig_total.write_html(graph_temp_file)

            # Descargar la gráfica como archivo
            return send_file(graph_temp_file, as_attachment=True)
        else:
            # Redirigir si el usuario no es un administrador
            return redirect(url_for('session.login'))
    else:
        # Redirigir si no hay sesión iniciada
        return redirect(url_for('session.login'))