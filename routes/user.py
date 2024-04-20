from flask import Blueprint, render_template, url_for, redirect, session

from functions.functions import get_user

import plotly.graph_objs as go

from plotly.offline import plot

import database.database as dbase

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


# Ruta para mostrar encuesta
@user_routes.route('/test/')
def test():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        user = get_user(email)
        if user:
            return render_template('test.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar encuesta en Español
@user_routes.route('/test/es/')
def testEs():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        user = get_user(email)
        if user:
            return render_template('testEs.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar encuesta en Nahuatl
@user_routes.route('/test/na/')
def testNa():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        user = get_user(email)
        if user:
            return render_template('testNa.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar encuesta en Mixteco
@user_routes.route('/test/mix/')
def testMix():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        user = get_user(email)
        if user:
            return render_template('testMix.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar encuesta en Tlapaneco
@user_routes.route('/test/tla/')
def testTla():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        user = get_user(email)
        if user:
            return render_template('testTla.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar encuesta en Portugues
@user_routes.route('/test/por/')
def testPor():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        user = get_user(email)
        if user:
            return render_template('testPor.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar encuesta en español
@user_routes.route('/test/fra/')
def testFra():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        user = get_user(email)
        if user:
            return render_template('testFra.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para mostrar resultados
@user_routes.route('/results/')
def results():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MongoDB
        user = get_user(email)
        if user:
            # Datos de ejemplo para la gráfica
            carreras = ['Tecnologías de la Información',
                        'Mantenimiento Industrial',
                        'Gastronomía',
                        'Desarrollo de Negocios']
            # Número de respuestas de ejemplo para cada carrera
            respuestas_ejemplo = [10, 5, 7, 2]

            # Crear el gráfico de barras con Plotly
            data = [go.Bar(x=carreras, y=respuestas_ejemplo)]

            # Configurar el diseño del gráfico
            layout = go.Layout(xaxis=dict(title='Carreras'),
                               yaxis=dict(title='Número de respuestas'))

            # Crear la figura
            fig = go.Figure(data=data, layout=layout)

            # Guardar el gráfico como un archivo HTML
            graph_html = plot(fig, output_type='div', include_plotlyjs=True)

            return render_template('results.html', graph=graph_html)
    else:
        return redirect(url_for('session.login'))
