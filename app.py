from flask import Flask, render_template

from routes.main import main_routes

from routes.session import session_routes

from routes.admin import admin_routes

from routes.user import user_routes

import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

# Registrar blueprints
app.register_blueprint(main_routes)

app.register_blueprint(session_routes)

app.register_blueprint(admin_routes)

app.register_blueprint(user_routes)

# Ruta para manejar páginas no encontradas
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
