import unittest
import os
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, setup_db
from config import SQLALCHEMY_TEST_DATABASE_URI


class CapstoneTestCase(unittest.TestCase):
    '''This class represents the capstone test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, SQLALCHEMY_TEST_DATABASE_URI)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        '''Executed after reach test'''
        pass

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_404_get_actors(self):
        res = self.client().get('/actors?page=999999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'actors not found')

    def test_create_actor(self):
        actor = {
            'name': 'Tiger Shroff',
            'gender': 'Male',
            'age': 30
        }

        res = self.client().post('/actors', json=actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_422_create_actor(self):
        actor = {
            'gender': 'Male'
        }

        res = self.client().post('/actors', json=actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'name cannot be blank')

    def test_patch_actor(self):
        actor_update = {
            'age': 56
        }

        res = self.client().patch('/actors/2', json=actor_update)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 2)

    def test_patch_404_actor(self):
        actor_update = {
            'age': 56
        }

        res = self.client().patch('/actors/99999', json=actor_update)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertTrue(data['error'], 404)
        self.assertTrue(data['message'], 'actor not found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 1)

    def test_delete_404_actor(self):
        res = self.client().delete('/actors/999999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'actor not found')

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_404_get_movies(self):
        res = self.client().get('/movies?page=999999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'], 'movies not found')

    def test_create_movie(self):
        movie = {
            'title': 'Kabhi Eid Kabhi Diwali',
            'release_year': '2021'
        }

        res = self.client().post('/movies', json=movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    # def test_patch_movie(self):
    #     movie = {
    #         'release_year': '2020'
    #     }
    #     res = self.client().patch('/movies/3', json=movie)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['updated'], 3)

    # def test_delete_movie(self):
    #     res = self.client().delete('/movies/1')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['deleted'], 1)

    # def test_delete_404_movie(self):
    #     res = self.client().delete('/movies/999999')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])
    #     self.assertEqual(data['error'], 404)
    #     self.assertEqual(data['message'], 'movie not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
