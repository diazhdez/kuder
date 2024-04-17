from flask import Flask

from routes.main import main_routes

from routes.session import session_routes

from routes.admin import admin_routes

from routes.user import user_routes

app = Flask(__name__)

app.secret_key = 'M0i1Xc$GfPw3Yz@2SbQ9lKpA5rJhDtE7'


# Registrar blueprints
app.register_blueprint(main_routes)

app.register_blueprint(session_routes)

app.register_blueprint(admin_routes)

app.register_blueprint(user_routes)


if __name__ == '__main__':
    app.run(debug=True)
