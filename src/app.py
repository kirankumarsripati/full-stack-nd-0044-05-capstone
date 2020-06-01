import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError
from models import setup_db


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

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'success': True,
            'message': 'Hello World'
        })

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
