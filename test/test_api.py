import unittest, json
from app import app

class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        
    def tearDown(self):
        pass


    def test_wired_up(self):
        with self.app as c:
            response = c.get('/')
            data = json.loads(response.data)
            self.assertSequenceEqual( {'success':'hello world'}, data )
