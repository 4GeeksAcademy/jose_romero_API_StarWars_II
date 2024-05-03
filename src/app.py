"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import Planet, db, User, Characters,Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#------CREAR UN USUARIO----------------
@app.route('/user', methods=['POST'])

def handle_create_user():
    new_user = User(email="romero@jose", password="password")
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "user": {
            "id": new_user.id,
            "email": new_user.email,
        },
        "msg": "El usuario ha sido creado exitosamente"
    }
    return jsonify(response_body), 200

#------------------------------------------

# -------TRAER A TODOS LOS USUARIOS-----
@app.route('/user', methods=['GET'])

def handle_user():
    users = User.query.all()
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    print (users)

    response_body = {
        "user": users_serialized
    }

    return jsonify(response_body), 200
#-----------------------------------------------
# LLAMAR A UN SOLO USUARIO

@app.route('/user/<int:id>', methods=['GET'])

def handle_one_user(id):
    user = User.query.get(id)

    response_body = {
        "users": user.serialize()
    }

    return jsonify(response_body), 200
#-------------------------------------------------
# ------BORRAR UN USUARIO --------------
@app.route('/user/<int:id>', methods=['DELETE'])
def handle_delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    for favorite in user.favorites:
        db.session.delete(favorite)

    response_body = {
       "msg":"Usuario eliminado Exitosamente"
    }
    return jsonify(response_body), 200

#-------------------------------------------------------------

#------CREAR UN CHARACTERS----------------
@app.route('/people', methods=['POST'])

def handle_create_character():
    new_character = Characters(name="Luke skywalker", gender="male", description="es un personaje ficticio de Star-Wars" )
    db.session.add(new_character)
    db.session.commit()

    response_body = {
        "character": {
            "name": new_character.name,
            "gender": new_character.gender,
            "description": new_character.description
        },
        "msg": "El personaje ha sido creado exitosamente"
    }
    return jsonify(response_body), 200
#---------------------------------------------------

#--------TRAER TODOS LOS CHARACTERS-----------
@app.route('/people', methods=['GET'])

def handle_people():
    people = Characters.query.all()
    Characters_serialized = []
    for peoples in people:
        Characters_serialized.append(peoples.serialize())
    print (people)

    response_body = {
        "Characters": Characters_serialized
    }

    return jsonify(response_body), 200
#-------------------------------------------------------

# LLAMAR A UN SOLO CHARACTER

@app.route('/people/<int:id>', methods=['GET'])

def handle_one_character(id):
    people = Characters.query.get(id)

    response_body = {
        "Characters": people.serialize()
    }

    return jsonify(response_body), 200

#-------------------------------------------

#----ELIMINAR UN CHARACTERS---- 
@app.route('/people/<int:id>', methods=['DELETE'])
def handle_delete_character(id):
    new_character = Characters.query.get(id)
    db.session.delete(new_character)
    db.session.commit()

    for favorite in new_character.favorites:
        db.session.delete(favorite)

    response_body = {
       "msg":"personaje eliminado Satisfactoriamente"
    }
    return jsonify(response_body), 200


# -------TRAER A TODOS LOS PLANETAS-----
@app.route('/planets/', methods=['GET'])

def handle_planets():
    planet = Planet.query.all()
    planet_serialized = []
    for planet in planet:
        planet_serialized.append(planet.serialize())
    print (planet)

    response_body = {
        "Planet": planet_serialized
    }

    return jsonify(response_body), 200
#------------------------------------------------

#---TRAER UN SOLO PLANETA---
@app.route('/planets/<int:id>', methods=['GET'])

def handle_one_planets(id):
    planet = Planet.query.get(id)
    print (planet)

    response_body = {
        "Planet": planet.serialize()
    }

    return jsonify(response_body), 200
#------------------------------------------------------------------

#----CREAR UN NUEVO PLANETA---- 
@app.route('/planets', methods=['POST'])
def handle_create_planet():
    new_planet = Planet( name ="saturno", description="planeta de 7 anillos",terrain="gaseoso" )
    db.session.add(new_planet)
    db.session.commit()

    response_body = {
        "planet": {
            "id": new_planet.id,
            "name": new_planet.name,
            "description": new_planet.description,
            "naterrainme": new_planet.terrain
        },
        "msg": "El planeta ha sido creado exitosamente"
    }
    return jsonify(response_body), 200
#--------------------------------------------------------

#--------ELIMINAR UN  PLANETA----------- 
@app.route('/planets/<int:id>', methods=['DELETE'])
def handle_delete_planet(id):
    new_planet = Planet.query.get(id)
    db.session.delete(new_planet)
    db.session.commit()

    for favorite in new_planet.favorites:
        db.session.delete(favorite)

    response_body = {
       "msg":"planeta eliminado"
    }
    return jsonify(response_body), 200


#------------------------------------------------------------
@app.route('/wipeall', methods=['GET'])
def database_wipe():
    try:
        db.reflect()
        db.drop_all()
        db.session.commit()
    except Exception as e:
        return "mec", 500
    return "ok", 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
