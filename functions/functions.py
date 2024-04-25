import database.database as dbase

db = dbase.dbConnection()


def get_user(email):
    user = db['users'].find_one({'email': email})
    return user


def get_admin(email):
    admin = db['admin'].find_one({'email': email})
    return admin


# Función para verificar si el usuario ha completado el cuestionario
def user_has_completed_survey(user_id):
    respuestas = db['respuestas']
    return respuestas.find_one({'user_id': str(user_id)}) is not None
