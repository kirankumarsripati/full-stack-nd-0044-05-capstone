import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

ITEMS_PER_PAGE = 10

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TEST_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')

AUTH0_DOMAIN = 'dev-jv5b18wv.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'FSND'