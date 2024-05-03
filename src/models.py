from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites = db.relationship('Favorites', backref='User', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email
    
    def __init__(self, email, password):
            self.email = email,
            self.password = password,
            self.is_active = True
        
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
#____________________________________________________________________________
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    terrain = db.Column(db.String(100), nullable=False)
    favorites = db.relationship('Favorites', backref='Planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id
    
    def __init__(self, name, description,terrain):
        self.name = name
        self.description = description
        self.terrain = terrain

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "terrain": self.terrain,
        }
#________________________________________________________________________________
class Characters(db.Model):
    id_characters = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    description = db.Column(db.String(300))
    favorites = db.relationship('Favorites', backref='Characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.id_characters
    
    def __init__(self, name, gender, description):
        self.name = name
        self.gender = gender
        self.description = description

    def serialize(self):
        return {
            "id_characters": self.id_characters,
            "name": self.name,
            "gender": self.gender,
            "description": self.description,
        }
#__________________________________________________________________________________________________
class Favorites(db.Model):
    id_Favorites = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id_characters'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.id_Favorites
    
    def __init__(self,id_Favorites, planet_id, character_id,user_id):
        self.id_Favorites = id_Favorites
        self.planet_id = planet_id
        self.character_id = character_id,
        self.user_id = user_id

    def serialize(self):
        return {
            "id_Favorites": self.id_Favorites,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "user_id": self.user_id,
        }