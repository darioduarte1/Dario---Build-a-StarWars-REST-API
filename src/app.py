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
from models import db, User, Characters, Planets, Spaceships,Favorites
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

# Ruta para GET de todos los users en la Base de Dados
@app.route('/users', methods=['GET'])
def get_users():
    users_query = User.query.all()
    users_text = [user.serialize() for user in users_query]
    return jsonify (users_text), 200

# Ruta para GET de un character especifico en la Base de Dados
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_favorites_user(user_id):
    favorites_query = Favorites.query.filter_by(user_fk=user_id)
    if favorites_query:
        response_body = {
            "msg": "Favorito encontrado",
            "result": [favorite.serialize() for favorite in favorites_query]
        }
        return jsonify (response_body), 200
    else:
        return jsonify ({"message": "Favorite no encontrado"}), 404
    

# Ruta para POST de un Planeta Favorito especifico en la Base de Dados
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorites_planet(planet_id):
    request_body = request.json
    planet = Planets.query.filter_by(id=planet_id).first()
    if planet is None: 
        return jsonify ({"message": "Planeta Favorito no encontrado"}), 404
    user = User.query.filter_by(id=request_body["user_id"]).first()
    if user is None: 
        return jsonify ({"message": "User no encontrado"}), 404

    planet_favorites = Favorites(user_fk=request_body["user_id"],planet_fk=planet_id)
    db.session.add(planet_favorites)
    db.session.commit()
    return jsonify ({"message": "Favorite creado con exito"}), 200

# Ruta para POST de un Character Favorito en la Base de Datos
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorites_people(people_id):
    request_body = request.json
    character = Characters.query.filter_by(id=people_id).first()
    if character is None: 
        return jsonify({"message": "Personaje Favorito no encontrado"}), 404
    user = User.query.filter_by(id=request_body["user_id"]).first()
    if user is None: 
        return jsonify({"message": "Usuario no encontrado"}), 404

    character_favorite = Favorites(user_fk=request_body["user_id"], characters_fk=people_id)
    db.session.add(character_favorite)
    db.session.commit()
    return jsonify({"message": "Favorito creado con éxito"}), 200

# Ruta para DELETE de un Character Favorito en la Base de Datos
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorites_people(people_id):
    request_body = request.json
    character = Characters.query.filter_by(id=people_id).first()
    if character is None: 
        return jsonify({"message": "Personaje Favorito no encontrado"}), 404
    user = User.query.filter_by(id=request_body["user_id"]).first()
    if user is None: 
        return jsonify({"message": "Usuario no encontrado"}), 404

    character_favorite = Favorites.query.filter_by(user_fk=request_body["user_id"],characters_fk=character.id).first()
    db.session.delete(character_favorite)
    db.session.commit()
    return jsonify({"message": "Favorito eliminado con éxito"}), 200

# Ruta para DELETE de un Planet Favorito en la Base de Datos
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorites_planet(planet_id):
    request_body = request.json
    planet = Planets.query.filter_by(id=planet_id).first()
    if planet is None: 
        return jsonify({"message": "Planeta Favorito no encontrado"}), 404
    user = User.query.filter_by(id=request_body["user_id"]).first()
    if user is None: 
        return jsonify({"message": "Usuario no encontrado"}), 404

    planet_favorite = Favorites.query.filter_by(user_fk=request_body["user_id"],planet_fk=planet.id).first()
    db.session.delete(planet_favorite)
    db.session.commit()
    return jsonify({"message": "Favorito eliminado con éxito"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
