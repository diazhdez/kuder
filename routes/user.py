from flask import Blueprint, render_template, url_for, redirect, session, request, send_file, jsonify

from functions.functions import get_user, user_has_completed_survey, user_has_completed_hubspot_form

import plotly.graph_objs as go

import plotly.io as pio

import mysql.connector

import database.database as dbase

db = dbase.dbConnection()

user_routes = Blueprint('user', __name__)


# Ruta para inicio de usuarios
@user_routes.route('/user/')
def user():
    if 'email' in session:
        email = session['email']
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            # Agregar una variable al contexto de la plantilla para indicar si el usuario ha completado algún test
            user['has_completed_survey'] = user_has_completed_survey(
                user['id'])
            return render_template('user.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Metodo para actulizar datos de un usuario
@user_routes.route('/update/', methods=['POST'])
def update():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        carrera = request.form.get('carrera')

        cursor = db.cursor()
        try:
            # Actualizar los datos del usuario en la base de datos
            cursor.execute(
                "UPDATE user SET name = %s, carrera = %s WHERE id = %s", (name, carrera, user_id))
            db.commit()
        except mysql.connector.Error as err:
            print("Error al actualizar datos del usuario:", err)
            db.rollback()
        finally:
            cursor.close()

    return redirect(url_for('user.user'))


# Ruta para mostrar test
@user_routes.route('/test/')
def test():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            if user_has_completed_survey(user['id']):
                return redirect(url_for('user.results'))
            else:
                return render_template('test.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar test en Español
@user_routes.route('/test/es/')
def testEs():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            if user_has_completed_survey(user['id']):
                return redirect(url_for('user.results'))
            else:
                return render_template('testEs.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar test en Nahuatl
@user_routes.route('/test/na/')
def testNa():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            if user_has_completed_survey(user['id']):
                return redirect(url_for('user.results'))
            else:
                return render_template('testNa.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar test en Mixteco
@user_routes.route('/test/mix/')
def testMix():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            if user_has_completed_survey(user['id']):
                return redirect(url_for('user.results'))
            else:
                return render_template('testMix.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar test en Tlapaneco
@user_routes.route('/test/tla/')
def testTla():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            if user_has_completed_survey(user['id']):
                return redirect(url_for('user.results'))
            else:
                return render_template('testTla.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar test en Portugues
@user_routes.route('/test/por/')
def testPor():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            if user_has_completed_survey(user['id']):
                return redirect(url_for('user.results'))
            else:
                return render_template('testPor.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para contestar test en Frances
@user_routes.route('/test/fra/')
def testFra():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            if user_has_completed_survey(user['id']):
                return redirect(url_for('user.results'))
            else:
                return render_template('testFra.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para mandar las respuestas
@user_routes.route('/guardar/', methods=['POST', 'GET'])
def guardar():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            if request.method == 'POST':
                cursor = db.cursor()
                try:
                    # Obtener los datos del formulario
                    user_id = request.form.get('user_id')
                    pregunta1 = request.form.get('pregunta1')
                    pregunta2 = request.form.get('pregunta2')
                    pregunta3 = request.form.get('pregunta3')
                    pregunta4 = request.form.get('pregunta4')
                    pregunta5 = request.form.get('pregunta5')
                    pregunta6 = request.form.get('pregunta6')
                    pregunta7 = request.form.get('pregunta7')
                    pregunta8 = request.form.get('pregunta8')
                    pregunta9 = request.form.get('pregunta9')
                    pregunta10 = request.form.get('pregunta10')
                    pregunta11 = request.form.get('pregunta11')
                    pregunta12 = request.form.get('pregunta12')
                    pregunta13 = request.form.get('pregunta13')
                    pregunta14 = request.form.get('pregunta14')
                    pregunta15 = request.form.get('pregunta15')
                    pregunta16 = request.form.get('pregunta16')
                    pregunta17 = request.form.get('pregunta17')
                    pregunta18 = request.form.get('pregunta18')
                    pregunta19 = request.form.get('pregunta19')
                    pregunta20 = request.form.get('pregunta20')
                    pregunta21 = request.form.get('pregunta21')
                    pregunta22 = request.form.get('pregunta22')
                    pregunta23 = request.form.get('pregunta23')
                    pregunta24 = request.form.get('pregunta24')

                    # Insertar las respuestas en la tabla de respuestas
                    cursor.execute("INSERT INTO answers (user_id, pregunta_1, pregunta_2, pregunta_3, pregunta_4, pregunta_5, pregunta_6, pregunta_7, pregunta_8, pregunta_9, pregunta_10, pregunta_11, pregunta_12, pregunta_13, pregunta_14, pregunta_15, pregunta_16, pregunta_17, pregunta_18, pregunta_19, pregunta_20, pregunta_21, pregunta_22, pregunta_23, pregunta_24) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                   (user_id, pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6, pregunta7, pregunta8, pregunta9, pregunta10, pregunta11, pregunta12, pregunta13, pregunta14, pregunta15, pregunta16, pregunta17, pregunta18, pregunta19, pregunta20, pregunta21, pregunta22, pregunta23, pregunta24))
                    db.commit()
                except mysql.connector.Error as err:
                    print("Error al guardar las respuestas:", err)
                    db.rollback()
                finally:
                    cursor.close()

                return redirect(url_for('user.results'))
        else:
            return redirect(url_for('session.login'))

    return redirect(url_for('user.test'))


# Ruta para mostrar resultados
@user_routes.route('/results/')
def results():
    if 'email' in session:
        email = session['email']
        # Función para obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            # Obtener el campo 'carrera' del usuario
            carrera_usuario = user.get('carrera')

            # Verificar si carrera_usuario es None y asignar un valor predeterminado si lo es
            carrera_usuario = carrera_usuario if carrera_usuario is not None else "Carrera no especificada"

            # Obtener el ID del usuario actual
            user_id = user['id']

            cursor = db.cursor(dictionary=True)
            try:
                # Obtener todas las respuestas del usuario actual desde la base de datos
                cursor.execute(
                    "SELECT * FROM answers WHERE user_id = %s", (user_id,))
                respuestas_usuario = cursor.fetchall()

                # Inicializar el contador de carreras
                carreras_count = {'TICS': 0,
                                  'Gastronomía': 0,
                                  'Mantenimiento Industrial': 0,
                                  'Desarrollo de Negocios': 0}

                # Iterar sobre todas las respuestas del usuario
                for respuesta in respuestas_usuario:
                    # Iterar sobre las preguntas en cada respuesta
                    for pregunta, carrera in respuesta.items():
                        # Verificar si la respuesta corresponde a una carrera
                        if pregunta.startswith('pregunta_') and carrera in carreras_count:
                            # Incrementar el contador de la carrera correspondiente
                            carreras_count[carrera] += 1

                # Crear el gráfico de barras con Plotly
                data = [go.Bar(x=list(carreras_count.keys()),
                               y=list(carreras_count.values()))]

                # Configurar el diseño del gráfico
                layout = go.Layout(title='Carrera a postularse: ' + carrera_usuario,  # Incorporar el campo carrera en el título
                                   xaxis=dict(title='Carreras'),
                                   yaxis=dict(title='Número de respuestas'))

                # Crear la figura
                fig = go.Figure(data=data, layout=layout)

                # Convertir la figura a HTML
                graph_html = fig.to_html(
                    full_html=False, include_plotlyjs='cdn')

                # Agregar una variable al contexto de la plantilla para indicar si el usuario ha completado algún test
                user['has_completed_survey'] = user_has_completed_survey(
                    user['id'])

                return render_template('results.html', graph=graph_html, user=user)
            except mysql.connector.Error as err:
                print("Error al obtener resultados:", err)
            finally:
                cursor.close()
    return redirect(url_for('session.login'))


@user_routes.route('/results/pdf')
def download_pdf():
    if 'email' in session:
        email = session['email']
        # Obtener datos del usuario desde MySQL
        user = get_user(email)
        if user:
            # Obtener el campo 'carrera' del usuario
            carrera_usuario = user.get('carrera', 'Carrera no especificada')

            # Obtener el ID del usuario actual
            user_id = user['id']

            # Obtener todas las respuestas del usuario actual desde la base de datos
            cursor = db.cursor(dictionary=True)
            try:
                cursor.execute(
                    "SELECT * FROM answers WHERE user_id = %s", (user_id,))
                respuestas_usuario = cursor.fetchall()

                # Inicializar el contador de carreras
                carreras_count = {'TICS': 0,
                                  'Gastronomía': 0,
                                  'Mantenimiento Industrial': 0,
                                  'Desarrollo de Negocios': 0}

                # Iterar sobre todas las respuestas del usuario
                for respuesta in respuestas_usuario:
                    # Iterar sobre las preguntas en cada respuesta
                    for pregunta, carrera in respuesta.items():
                        # Verificar si la respuesta corresponde a una carrera
                        if pregunta.startswith('pregunta_') and carrera in carreras_count:
                            # Incrementar el contador de la carrera correspondiente
                            carreras_count[carrera] += 1

                # Crear el gráfico de barras con Plotly
                data = [go.Bar(x=list(carreras_count.keys()),
                               y=list(carreras_count.values()))]

                # Configurar el diseño del gráfico
                layout = go.Layout(title='Carrera a postularse: ' + carrera_usuario,  # Incorporar el campo carrera en el título
                                   xaxis=dict(title='Carreras'),
                                   yaxis=dict(title='Número de respuestas'))

                # Crear la figura
                fig = go.Figure(data=data, layout=layout)

                # Guardar la figura como PDF temporalmente
                temp_pdf_path = "resultados.pdf"
                pio.write_image(fig, temp_pdf_path, format="pdf")

                # Enviar el archivo PDF al usuario para su descarga
                return send_file(temp_pdf_path, as_attachment=True)
            except mysql.connector.Error as err:
                print("Error al obtener resultados para descarga PDF:", err)
            finally:
                cursor.close()
    return redirect(url_for('session.login'))


# Ruta para mostrar el formulario de hubspot
@user_routes.route('/hubspot/')
def hubspot():
    if 'email' in session:
        email = session['email']
        user = get_user(email)
        if user:
            if user_has_completed_hubspot_form(user['id']):
                # Redirige si ya ha completado el formulario de HubSpot
                return redirect(url_for('user.test'))
            else:
                user['has_completed_survey'] = user_has_completed_survey(
                    user['id'])
                return render_template('hubspot.html', user=user)
    else:
        return redirect(url_for('session.login'))


# Ruta para guardar los datos del formulario en la colección hubspot
@user_routes.route('/save_form_data', methods=['POST'])
def save_form_data():
    # Obtener el ID del usuario de la sesión
    user_id = db.user['user_id']

    # Obtener los datos del formulario enviados desde el cliente
    form_data = request.json

    # Agregar el ID del usuario a los datos del formulario
    form_data['user_id'] = user_id

    # Insertar los datos del formulario en la colección hubspot de MySQL
    try:
        db.hubspot.insert_one(form_data)
        return jsonify({"message": "Datos del formulario guardados exitosamente en la colección 'hubspot'"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
