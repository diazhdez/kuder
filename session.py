from flask import Blueprint, render_template, url_for, redirect, flash, session, request

import bcrypt

import database as dbase

db = dbase.dbConnection()

session_routes = Blueprint('session', __name__)


# Ruta de Inicio de sesión
@session_routes.route('/login/')
def login():
    return render_template('login.html')


@session_routes.route('/iniciar/', methods=['POST'])
def iniciar():
    admin = db['admin']
    users = db['users']
    email = request.form['email']
    password = request.form['password']

    # Buscar en la colección de admin
    login_user = users.find_one({'email': email})
    if login_user and bcrypt.checkpw(password.encode('utf-8'), login_user['password']):
        session['email'] = email
        return redirect(url_for('user.user'))

    # Buscar en la colección de admin
    login_admin = admin.find_one({'email': email, 'password': password})
    if login_admin:
        session['email'] = email
        return redirect(url_for('admin.admin'))

    flash('Correo o contraseña incorrectos')
    return redirect(url_for('session.login'))


# Ruta para cerrar sesión
@session_routes.route('/logout/')
def logout():
    session.clear()  # Elimina todas las variables de sesión
    return redirect(url_for('index'))
