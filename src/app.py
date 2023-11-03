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
from models import db, User, People, Planets, Favorites
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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


#  Listar todos los registros de people en la base de datos
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people = list(map(lambda item: item.serialize(), people))

    return jsonify(people)


# Listar la información de una sola people
@app.route('/people/<int:id>', methods=['GET'])
def get_people_id(id=None): #asegurar darle un valor al id (buenas practicas)
    people = People.query.get(id)

    return jsonify(people)


# Listar los registros de planets en la base de datos
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = People.query.all()
    planets = list(map(lambda item: item.serialize(), planets))

    return jsonify(planets)


# Listar la información de un solo planet
@app.route('/planets/<int:id>', methods=['GET'])
def get_planets_id(id=None):
    planets = Planets.query.get(id)

    return jsonify(planets)


# Listar todos los usuarios del blog
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda item: item.serialize(), users))

    return jsonify(users)


# Listar todos los favoritos que pertenecen al usuario actual
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_users_favorites(user_id=None):
    favorites = Favorites.query.filter_by(user_id = user_id).all()
    if favorites is None:
        return jsonify({'msg': "not found favorites"}), 404
    else:
        favorites = list(map(lambda item:item.serialize(), favorites))
        return jsonify(favorites)
    

# Añade un nuevo planet favorito al usuario actual con el planet id = planet_id.
@app.route('/favorites/planets/<int:planets_id>', methods=['POST'])
def add_planet_user(planets_id): #si el endpoint tiene una parte dinamica(planets_id), debo colocarselo como parametrp a la funcion
    body = request.json #.json no lleva parentesis -> obtengo lo que envio por body desde thunder
    user_id = body.get('user_id')
    # planets_id = body.get('planets_id') -> que me envia por el body?
    if user_id is None or planets_id is None:
        return jsonify({'msg': 'planets_id and user_id is requery'}), 400
    #aqui si lo consulto en la base de datos
    favorites = Favorites.query.filter_by(user_id = user_id, planets_id = planets_id).first()
    if favorites: #is not none (ambas sirven)
        return jsonify({'msg': 'this favorite exist'})
    #instanciar la clase
    favorites = Favorites(user_id = body.get('user_id'), planets_id = planets_id)
                                                #planets_id = body.get('planets_id') -> esto si lo agrego desde el body
    #un paso para añadir a la base de datos (como git add .)
    db.session.add(favorites)
    try: 
        db.session.commit() #aqui se agregó
        return jsonify({'msg': 'se agrego el favorito'})
    except Exception as error:
        return jsonify({'msg': f'{error}'}), 500
    

# Añade una nueva people favorita al usuario actual con el people.id = people_id.
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people(people_id):
    body = request.json
    user_id = body.get('user_id')
    if user_id is None or people_id is None:
        return jsonify({'msg': 'people_id and user_id is requery'}), 400
    favorites = Favorites.query.filter_by(user_id = user_id, people_id = people_id).first()
    db.session.add(favorites)
    try: 
        db.session.commit() #aqui se agregó
        return jsonify({'msg': 'se agrego la people favorito'})
    except Exception as error:
        return jsonify({'msg': f'{error}'}), 500


# Elimina un planet favorito con el id = planet_id`.
@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=["DELETE"])
#delete NO acepta body
def delete_planets(planet_id, user_id):
    #consulta a la db
    favorites = Favorites.query.filter_by(planets_id = planet_id, user_id = user_id).first()
    #planets_id -> tiene que coincidir con el nombre de la columna del modelo
    #planet_id -> tiene que coincidir con el parametro y la URL
    if favorites is None:
        return jsonify({'msg': 'este favorito no existe'}), 404
    db.session.delete(favorites)
    try: #para asegurar si algo falla -> por eso el commit va dentro del try
        db.session.commit()
        return jsonify({'msg': 'el favorito se elimino'})
    except Exception as error:
        return jsonify({'msg': f'{error}'}), 500


@app.route('/favorite/people/<int:people_id>', methods=["DELETE"])
def delete_people(people_id, user_id):
    favorites = Favorites.query.filter_by(people_id = people_id, user_id = user_id).first()
    if favorites is None:
        return jsonify({'msg': 'este favorito no existe'}), 404
    # se prepara para borrar
    db.session.delete(favorites)
    try: #para asegurar si algo falla -> por eso el commit va dentro del try
        db.session.commit() #aqui se borro
        return jsonify({'msg': 'el favorito se elimino'})
    except Exception as error:
        return jsonify({'msg': f'{error}'}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
