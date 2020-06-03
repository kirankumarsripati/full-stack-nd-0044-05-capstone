import unittest
import os
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, setup_db
from config import SQLALCHEMY_TEST_DATABASE_URI

tokens = {
    'casting_assistant': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZEVNVE0yUVRsRE9UUXhNVEl5UVRZek5VUXpPVEZHT1VSRE1FUkNSRGd6TWtZMU5qUTVPQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdjViMTh3di5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTczOTE0NjY4OTE4NDk4OTQ4MjUiLCJhdWQiOiJGU05EIiwiaWF0IjoxNTkxMTc0Mjg0LCJleHAiOjE1OTEyNjA2ODQsImF6cCI6IjVKMTRCRmJxSmRibEc0QnNodWhuZVIzeEdlZXJiSm12Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.EeDb5yhOdNM_Ukbkh9ttDQQFtmfrIizlPzVitJFczTcqK28t69AC3n5I_3euWMtKFCndntWOzKXZO4j7UeuX9aAJCv2_JGKEalIU3l0AAsKUpJ_rXY7ODZRo3X3gezJmZnnTDDRUEa1wxsTvXUQLJftlSKnIix-DZSxiacYvnZ2r3h9NEyeOTT5ESFMjitkn-NoUqKupnqgU_knu4v0Z0Jije7xPev3O-bzllu2PZG7L9WImOitZ4c4sg0ME5LFCH71qZxMficsYhFadV9kf1Fkbh4nAwJKniJXg8QdewL2LABXNBO0mfCSvYnGxbwSsEZE1sRUEsUByIg_ztUEn-A',
    'casting_director': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZEVNVE0yUVRsRE9UUXhNVEl5UVRZek5VUXpPVEZHT1VSRE1FUkNSRGd6TWtZMU5qUTVPQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdjViMTh3di5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTM2NDI2OTg2NTY3NTY2MjM1MDciLCJhdWQiOiJGU05EIiwiaWF0IjoxNTkxMTc0MDI5LCJleHAiOjE1OTEyNjA0MjksImF6cCI6IjVKMTRCRmJxSmRibEc0QnNodWhuZVIzeEdlZXJiSm12Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.RlM4x43bX_Kw44dNxrSxNnB4uEmKJzF4bgCEWCHvLH1qN3z3BsrY_yBbtGfzp4Q6GBY0oIReiVj3lsjaGffWrs1wL5gAyfWVUYUztSgxQFIZg6HClUQQREeXIv7YHvDJdcKf3as4nN6A5HIQL7AbdkYfQwUOl46ALlVnyaqTCjp97Id5pEW2o4XCy7hbdMoAn10nnI2shdGKFSk_KahDnhVUCZkY8MeewhKsE3QALh1psrfjcAX4BsdMtrxNj4ga-hcw59W-oLFArfZNrjcaNqqrTIeQKexu6q_k1lC9GVr8xw_ERELuae064lcJRr8kKqPek88Qg_KSbQgQg12ybw',
    'executive_producer':
    'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZEVNVE0yUVRsRE9UUXhNVEl5UVRZek5VUXpPVEZHT1VSRE1FUkNSRGd6TWtZMU5qUTVPQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdjViMTh3di5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTQzNzk5MzYyOTc4MTI1NjM1MzAiLCJhdWQiOiJGU05EIiwiaWF0IjoxNTkxMTc0MTM1LCJleHAiOjE1OTEyNjA1MzUsImF6cCI6IjVKMTRCRmJxSmRibEc0QnNodWhuZVIzeEdlZXJiSm12Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiY3JlYXRlOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZWRpdDphY3RvcnMiLCJlZGl0Om1vdmllcyIsInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.rPj_XLDtdPfo1lUvXKILHS4S-t9xmY3aZE8-EGdXHctrXUvdoDFMVzRM4JQf6-w-NrgfTBnS4R3E2Ku12Q0s7MxOfh8zZmD12ZWlcymk9bxz2sU1yCvs9Ft7TiusYU20gbod64mzAlsPtDPwYeOZ_cfR4T6S4PDEaVM9xJXpM1ByO4CE8f4OABZx89FIibOLhAnWP1M7p3ZlcLKsKd7rqhdSzGWghdgKjFbcNMscIh_i_EnS9db0jhPzqa2CcfT80gn3PPpj-a2AomW8NTc4M_ZFBn80TmcgjxS1hEAEAq0oew-7tpZxrkHlki5dufMs8a9oBixL3ViMuGE3Fmm_lw'
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
