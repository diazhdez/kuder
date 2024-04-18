from flask import Blueprint, render_template, url_for, redirect, session

import plotly.graph_objs as go

from plotly.offline import plot

from functions.functions import get_user

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
            layout = go.Layout(title='Resultados de la encuesta', xaxis=dict(
                title='Carreras'), yaxis=dict(title='Número de respuestas'))

            # Crear la figura
            fig = go.Figure(data=data, layout=layout)

            # Guardar el gráfico como un archivo HTML
            graph_html = plot(fig, output_type='div', include_plotlyjs=True)

            return render_template('results.html', graph=graph_html)
    else:
        return redirect(url_for('session.login'))
