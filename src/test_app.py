import unittest
import os
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, setup_db
from config import SQLALCHEMY_TEST_DATABASE_URI

tokens = {
    'casting_assistant': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZEVNVE0yUVRsRE9UUXhNVEl5UVRZek5VUXpPVEZHT1VSRE1FUkNSRGd6TWtZMU5qUTVPQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdjViMTh3di5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTczOTE0NjY4OTE4NDk4OTQ4MjUiLCJhdWQiOiJGU05EIiwiaWF0IjoxNTkxMTI4OTAwLCJleHAiOjE1OTEyMTUzMDAsImF6cCI6IjVKMTRCRmJxSmRibEc0QnNodWhuZVIzeEdlZXJiSm12Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.e5QkIc_GB-dJD2RhKsSZ1ulaIdqQr8WeHFjdfreyrvroSS-zIg7kcz7ZsGHtAcqbzSGRVPZjmhmAw7CytKezYv6l949PSD2PP6jPuM21fYEu5PkKZnpdmq9giFvcxZxq7yYTHpqPEOVEbabZ6hrF2GSSyRSHGJL8V9JddPwhtLQSb33o03nhGXefgj-EVm82fM3JAy1j0AkaCj99BTn6_ZXbHpruRjR6OznWyD_1-d9yAIakBRC-wYunUz6l92eCjCOvhh5QaHgciUQk7gifybtCHtungdFLsndbZ_1ksfVCeuLjVoU5YxEf8UcZNdzZmowQPhmtVOD2AwvCkp3KyQ',
    'casting_director': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZEVNVE0yUVRsRE9UUXhNVEl5UVRZek5VUXpPVEZHT1VSRE1FUkNSRGd6TWtZMU5qUTVPQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdjViMTh3di5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTM2NDI2OTg2NTY3NTY2MjM1MDciLCJhdWQiOiJGU05EIiwiaWF0IjoxNTkxMTI5MDQyLCJleHAiOjE1OTEyMTU0NDIsImF6cCI6IjVKMTRCRmJxSmRibEc0QnNodWhuZVIzeEdlZXJiSm12Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.LGtGSY2AAy_Fftyp18jOkYBvqD9LE_1527jB6R6LI-b40Dh2jFZijuy6iAdIrwvsW3BBTufXBo7Fbhw96FlExHIM9JsKtAzd76z7HiRDpPaqu0uGIoXkUIEoSXDBowipNq4aOLNsJnj9_HCAU0WgGTceWma8WE9KhdxzWKErXOQJGr9ol_Qt3CXnatpA5aWoTyTsXD5FqDxaok6yKFBc4gikhG1VS3jRZFCJ0MjrUwheCJrxKl2Tuk9WmrHrvjJjjaAHqgfQ0oHa_hVTcHKLGUh0-MZTAaGYaQbvfzXeDpLBUuudgYugd-lpYeNoGEGC1lbJigpNxEVYP4l8zPJwDA',
    'executive_producer':
    'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZEVNVE0yUVRsRE9UUXhNVEl5UVRZek5VUXpPVEZHT1VSRE1FUkNSRGd6TWtZMU5qUTVPQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdjViMTh3di5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTQzNzk5MzYyOTc4MTI1NjM1MzAiLCJhdWQiOiJGU05EIiwiaWF0IjoxNTkxMTI5MzgxLCJleHAiOjE1OTEyMTU3ODEsImF6cCI6IjVKMTRCRmJxSmRibEc0QnNodWhuZVIzeEdlZXJiSm12Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiY3JlYXRlOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZWRpdDphY3RvcnMiLCJlZGl0Om1vdmllcyIsInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.Wxlr9riHGefoFOBJ_a8VwtgbeXxfC-u9U81Yo1xNPUKqKdP-VzTtwDKYFvG5DgOrPfc9_aV4f3xtFJApcTZCsvZ9a0Ap-GAnWk1kmkfhsfXbDjPy5j7hOb9Fyi7ELPjhUZgHDeiH_S14PiJ5G3UOCGR2tiDhH5sunAL9gAZDyRPrJ40hwUG9PWi4avSBz3aRZTH0KJywMl64AizQt1-H1ssHPgTafrh01BFzgtjjrIWQ_Hib28vC5aPwZ5wiVcLu68GNeA0780XbduE74PwxCX7qYcZLkkn5XZgx8HXcXES9e_e4uRydgEtpaOlN26CL5z1Np7TglhlH8TwmnO7xSg'
}

headers_casting_assistant = {
    'Authorization': tokens['casting_assistant']
}

headers_casting_director = {
    'Authorization': tokens['casting_director']
}

headers_executive_producer = {
    'Authorization': tokens['executive_producer']
}


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

    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'], 'Authorization header is expected')

    def test_get_actors(self):
        res = self.client().get('/actors', headers=headers_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_404_get_actors(self):
        res = self.client().get('/actors?page=999999',
                                headers=headers_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'actors not found')

    def test_401_create_actor(self):
        actor = {
            'name': 'Tiger Shroff',
            'gender': 'Male',
            'age': 30
        }

        res = self.client().post('/actors', json=actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'],
                        'Authorization header is expected')

    def test_create_actor(self):
        actor = {
            'name': 'Tiger Shroff',
            'gender': 'Male',
            'age': 30
        }

        res = self.client().post('/actors',
                                 json=actor,
                                 headers=headers_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_422_create_actor(self):
        actor = {
            'gender': 'Male'
        }

        res = self.client().post('/actors',
                                 json=actor,
                                 headers=headers_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'name cannot be blank')

    def test_edit_actor(self):
        actor_update = {
            'age': 56
        }

        res = self.client().patch('/actors/2',
                                  json=actor_update,
                                  headers=headers_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 2)

    def test_edit_404_actor(self):
        actor_update = {
            'age': 56
        }

        res = self.client().patch('/actors/99999',
                                  json=actor_update,
                                  headers=headers_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertTrue(data['error'], 404)
        self.assertTrue(data['message'], 'actor not found')

    def test_401_edit_actor(self):
        actor_update = {
            'age': 56
        }

        res = self.client().patch('/actors/2',
                                  json=actor_update,
                                  headers=headers_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'],
                        'Permission not found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/1',
                                   headers=headers_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 1)

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/999999',
                                   headers=headers_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'actor not found')

    def test_401_delete_actor(self):
        res = self.client().delete('/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Authorization header is expected')

    def test_401_permission_delete_actor(self):
        res = self.client().delete('/actors/1',
                                   headers=headers_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers=headers_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_404_get_movies(self):
        res = self.client().get('/movies?page=999999',
                                headers=headers_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'], 'movies not found')

    def test_error_401_get_movies(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'], 'Authorization header is expected')

    def test_create_movie(self):
        movie = {
            'title': 'Kabhi Eid Kabhi Diwali',
            'release_year': 2021
        }

        res = self.client().post('/movies',
                                 json=movie,
                                 headers=headers_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_error_422_create_movie(self):
        movie = {
            'release_year': 2022
        }

        res = self.client().post('/movies',
                                 json=movie,
                                 headers=headers_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'title cannot be blank')

    def test_edit_movie(self):
        movie = {
            'release_year': 2020
        }
        res = self.client().patch('/movies/3',
                                  json=movie,
                                  headers=headers_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 3)

    def test_error_422_edit_movie(self):
        res = self.client().patch('/movies/3',
                                  headers=headers_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'invalid body JSON')

    def test_error_404_edit_movie(self):
        movie = {
            'release_year': 2020
        }
        res = self.client().patch('/movies/999999',
                                  json=movie,
                                  headers=headers_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'movie not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/10',
                                   headers=headers_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 10)

    def test_delete_404_movie(self):
        res = self.client().delete('/movies/999999',
                                   headers=headers_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'movie not found')

    def test_error_401_delete_movie(self):
        res = self.client().delete('/movies/6')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected')

    def test_error_401_delete_movie(self):
        res = self.client().delete('/movies/6',
                                   headers=headers_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
