from flask import Flask

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


if __name__ == '__main__':
    app.run(debug=True)
