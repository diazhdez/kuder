from flask import Blueprint, render_template

main_routes = Blueprint('main', __name__)


# Ruta principal
@main_routes.route('/')
def index():
    return render_template('index.html')


# Ruta de contacto
@main_routes.route('/contact')
def contact():
    return render_template('contact.html')
