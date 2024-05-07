from flask import Blueprint, render_template, url_for, redirect, flash, session, request, make_response

from functions.functions import get_admin

from datetime import datetime

from random import randint

from bson import ObjectId

import bcrypt

import database.database as dbase

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
                    hashpass = bcrypt.hashpw(
                        password.encode('utf-8'), bcrypt.gensalt())
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
                        {'firstname': {'$regex': search_query, '$options': 'i'}},
                        {'lastname': {'$regex': search_query, '$options': 'i'}},
                        {'email': {'$regex': search_query, '$options': 'i'}},
                        {'carrera_a_postulars': {
                            '$regex': search_query, '$options': 'i'}}
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
@admin_routes.route('/deleteUser/<string:user_id>/')
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
@admin_routes.route('/deleteAdmin/<string:admin_id>/')
def delete_admin(admin_id):
    admin = db['admin']
    admin.delete_one({'_id': ObjectId(admin_id)})
    return redirect(url_for('admin.admins'))


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


@admin_routes.route('/admin/results/graph/<user_id>')
def admin_results_graph_individual(user_id):
    if 'email' not in session:
        return redirect(url_for('session.login'))

    email = session['email']
    admin = get_admin(email)

    if not admin:
        return redirect(url_for('session.login'))

    usuario = db['users'].find_one({'_id': ObjectId(user_id)})
    if not usuario:
        return "Usuario no encontrado"

    carrera_usuario = usuario.get('carrera_a_postulars', 'Carrera no especificada')

    carreras_count = {'TICS': 0,
                      'Gastronomía': 0,
                      'Mantenimiento Industrial': 0,
                      'Desarrollo de Negocios': 0}

    respuestas_usuario = db.respuestas.find({'user_id': str(user_id)})

    for respuesta in respuestas_usuario:
        for pregunta, carrera in respuesta.items():
            if pregunta.startswith('pregunta_') and carrera in carreras_count:
                carreras_count[carrera] += 1

    data = [go.Bar(x=list(carreras_count.keys()),
                   y=list(carreras_count.values()))]

    layout = go.Layout(title=f'Carreras del usuario - {carrera_usuario}',
                       xaxis=dict(title='Carreras'),
                       yaxis=dict(title='Número de respuestas'))

    fig = go.Figure(data=data, layout=layout)

    # Convertir la figura a HTML
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Convertir el HTML a bytes
    graph_bytes = graph_html.encode()

    # Crear un objeto BytesIO a partir de los bytes
    from io import BytesIO
    graph_bytes_io = BytesIO(graph_bytes)

    # Mover el cursor al principio del objeto BytesIO
    graph_bytes_io.seek(0)

    # Crear una respuesta Flask
    response = make_response(graph_bytes_io.getvalue())

    # Establecer el tipo de contenido y la cabecera de descarga
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = f'attachment; filename=graph_user_{user_id}.html'

    return response