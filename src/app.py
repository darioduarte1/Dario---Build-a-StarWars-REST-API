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
from models import db, User, Characters, Planets, Spaceships
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

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Ruta para GET de todos los people en la Base de Dados
@app.route('/people', methods=['GET'])
def get_people():
    characters_query = Characters.query.all()
    characters_text = [character.serialize() for character in characters_query]
    return jsonify (characters_text), 200

# Ruta para GET de un character especifico en la Base de Dados
@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    characters_query = Characters.query.filter_by(id=people_id).first()
    if characters_query:
        response_body = {
            "msg": "Character encontrado",
            "result": characters_query.serialize()
        }
        return jsonify (response_body), 200
    else:
        return jsonify ({"message": "Character no encontrado"}), 404

# Ruta para GET de todos los planetas en la Base de Dados
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets_query = Planets.query.all()
    planets_text = [planet.serialize() for planet in planets_query]
    return jsonify (planets_text), 200

# Ruta para GET de un planeta especifico en la Base de Dados
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet_query = Planets.query.filter_by(id=planet_id).first()
    if planet_query:
        response_body = {
            "msg": "Planet encontrado",
            "result": planet_query.serialize()
        }
        return jsonify (response_body), 200
    else:
        return jsonify ({"message": "Planet no encontrado"}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
