from flask import Blueprint, render_template, url_for, redirect, session

from functions import get_user

import database as dbase

db = dbase.dbConnection()

user_routes = Blueprint('user', __name__)


# Ruta para inicio de usuarios
@user_routes.route('/user/')
def user():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        user = get_user(email)
        if user:
            return render_template('user.html', user=user)
    else:
        return redirect(url_for('session.login'))
    

@user_routes.route('/test/')
def test():
    return render_template('test.html')
