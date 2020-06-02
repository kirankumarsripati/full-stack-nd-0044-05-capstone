import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError
from models import setup_db, Actor, Movie
from config import ITEMS_PER_PAGE


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/actors', methods=['GET'])
    def get_actors():
        page = request.args.get('page', 1, type=int)
        selection = Actor.query.order_by(Actor.id).paginate(
            page,
            ITEMS_PER_PAGE,
            False
        )

        selection_array = [actor.format() for actor in selection.items]

        if len(selection_array) == 0:
            abort(404, {'message': 'actors not found'})

        return jsonify({
            'success': True,
            'actors': selection_array,
            'total': selection.total
        })

    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()

        if not body:
            abort(422, {'message': 'invalid body JSON'})

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', 'Other')

        if not name:
            abort(422, {'message': 'name cannot be blank'})

        if not age:
            abort(422, {'message': 'age cannot be blank'})

        try:
            actor = Actor(
                name=name,
                age=age,
                gender=gender
            )
            actor.insert()

        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'created': actor.id,
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def patch_actor(actor_id):
        body = request.get_json()

        if not body:
            abort(422, {'message': 'invalid body JSON'})

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404, {'message': 'actor not found'})

        try:
            actor.name = body.get('name', actor.name)
            actor.age = body.get('age', actor.age)
            actor.gender = body.get('gender', actor.gender)

            actor.update()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'updated': actor.id,
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404, {'message': 'actor not found'})

        try:
            actor.delete()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': actor_id,
        })

    @app.route('/movies', methods=['GET'])
    def get_movies():
        page = request.args.get('page', 1, type=int)
        selection = Movie.query.order_by(Movie.id).paginate(
            page,
            ITEMS_PER_PAGE,
            False
        )

        if len(selection.items) == 0:
            abort(404, {'message': 'movies not found'})

        selection_array = [movie.format() for movie in selection.items]

        return jsonify({
            'success': True,
            'movies': selection_array,
            'total': selection.total
        })

    @app.route('/movies', methods=['POST'])
    def create_movies():
        body = request.get_json()

        if not body:
            abort(422, {'message': 'invalid body JSON'})

        title = body.get('title', None)
        release_year = body.get('release_year', None)

        if not title:
            abort(422, {'message': 'title cannot be blank'})

        if not release_year:
            abort(422, {'message': 'release_year cannot be blank'})

        try:
            movie = Movie(
                title=title,
                release_year=release_year
            )
            movie.insert()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'created': movie.id,
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def patch_movie(movie_id):
        body = request.get_json()

        if not body:
            abort(422, {'message': 'invalid body JSON'})

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404, {'message': 'actor not found'})

        try:
            movie.title = body.get('title', movie.title)
            movie.release_year = body.get('release_year', movie.release_year)
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'updated': movie.id,
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404, {'message': 'movie not found'})

        try:
            movie.delete()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    @app.errorhandler(400)
    def bad_request(error):
        '''Error handler for bad request'''
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(e):
        '''Error handler for AuthError'''
        return jsonify({
            'success': False,
            'error': e.status_code,
            'message': e.error
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        '''Error handler for 404'''
        return jsonify({
            'success': False,
            'error': 404,
            'message': get_error_message(error, 'resource not found')
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        '''Error handling for unprocessable entity'''
        return jsonify({
            'success': False,
            'error': 422,
            'message': get_error_message(error, 'unprocessable')
        }), 422

    def get_error_message(error, default_message):
        '''
        Returns if there is any error message provided in
        error.description.message else default_message
        This can be passed by calling
        abort(404, description={'message': 'your message'})

        Parameters:
        error (werkzeug.exceptions.NotFound): error object
        default_message (str): default message if custom message not available

        Returns:
        str: Custom error message or default error message
        '''
        try:
            return error.description['message']
        except TypeError:
            return default_message

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
