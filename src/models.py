from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate


db = SQLAlchemy()


def setup_db(app, database_path=SQLALCHEMY_DATABASE_URI):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    migrate = Migrate(app, db)
    db.app = app
    db.init_app(app)
    return


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_year = db.Column(db.Integer)

    def __init__(self, title, release_year):
        self.title = title
        self.release_year = release_year

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete()
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year
        }

