import unittest

from app import create_app


class CapstoneTestCase(unittest.TestCase):
    '''This class represents the capstone test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        '''Executed after reach test'''
        pass

    def test_hello_world(self):
        string = 'hello world'
        self.assertEqual(string, 'hello world')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
