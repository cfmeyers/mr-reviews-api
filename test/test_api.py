import unittest, json
from app import app#, Review

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

    # def test_review_to_dict_method(self):
    #     review_info = {'item_author':'Jorge Luis Borges', 'item_title':'Labrynthes'}
    #     review1 = Review(**review_info)
    #     self.assertDictEqual(review_info, review1.to_dict)
