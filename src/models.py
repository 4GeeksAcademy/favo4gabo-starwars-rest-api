from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user')
    #el backref lo que hace es que pueda usar las propiedades de la tabla desde la tabla donde lo estoy relacionando
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'favorites': list(map(lambda favorites: favorites.serialize(), self.favorites))
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    eye_color = db.Column(db.String(100), unique=True, nullable=False)
    skin_color = db.Column(db.String(100), unique=True, nullable=False)
    favorites = db.relationship('Favorites', backref='people')
    #el backref lo que hace es que pueda usar las propiedades de la tabla desde la tabla donde lo estoy relacionando
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'eye_collor': self.eye_color,
            'skin_color': self.skin_color,
            'favorites': list(map(lambda favorites: favorites.serialize(), self.favorites))
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    rotation_period = db.Column(db.String(100), unique=True, nullable=False)
    climate = db.Column(db.String(100), unique=True, nullable=False)
    terrain = db.Column(db.String(100), unique=True, nullable=False)
    favorites = db.relationship('Favorites', backref='planets')
    #el backref lo que hace es que pueda usar las propiedades de la tabla desde la tabla donde lo estoy relacionando
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'rotation_period': self.rotation_period,
            'climate': self.climate,
            'terrain': self.terrain,
            'favorites': list(map(lambda favorites: favorites.serialize(), self.favorites))
        }
    

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planets_id": self.planets_id
            # do not serialize the password, its a security breach
        }