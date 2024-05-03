from flask import Blueprint, render_template, url_for, redirect, flash, session, request

import bcrypt

import mysql.connector

import database.database as dbase

# Obtener la conexión a la base de datos
db = dbase.dbConnection()

session_routes = Blueprint('session', __name__)


# Ruta de Inicio de sesión
@session_routes.route('/login/')
def login():
    if 'email' in session:
        email = session['email']
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
            admin = cursor.fetchone()
            if admin:
                return redirect(url_for('admin.admin'))

            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return redirect(url_for('user.user'))
        except mysql.connector.Error as err:
            print("Error al buscar usuario o administrador:", err)
        finally:
            cursor.close()
    # Si el usuario no está autenticado o no se encontró un usuario o administrador correspondiente,
    # renderiza el formulario de inicio de sesión
    return render_template('login.html')


# Ruta para iniciar usuario o admin
@session_routes.route('/iniciar/', methods=['POST'])
def iniciar():
    cursor = db.cursor(dictionary=True)
    try:
        email = request.form['email']
        password = request.form['password']

        # Buscar en la tabla de users
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        login_user = cursor.fetchone()
        if login_user and bcrypt.checkpw(password.encode('utf-8'), login_user['password'].encode('utf-8')):
            session['email'] = email
            return redirect(url_for('user.user'))

        # Buscar en la tabla de admin
        cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
        login_admin = cursor.fetchone()
        if login_admin and bcrypt.checkpw(password.encode('utf-8'), login_admin['password'].encode('utf-8')):
            session['email'] = email
            return redirect(url_for('admin.admin'))

        flash('Correo o contraseña incorrectos')
        return redirect(url_for('session.login'))
    except mysql.connector.Error as err:
        print("Error al iniciar sesión:", err)
    finally:
        cursor.close()


# Ruta para cerrar sesión
@session_routes.route('/logout/')
def logout():
    session.clear()  # Elimina todas las variables de sesión
    return redirect(url_for('main.index'))
