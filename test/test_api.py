import unittest, json
from app import app, db, Review
from ipdb import set_trace


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/marginal-review-test'
        self.app = app.test_client()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_wired_up(self):
        with self.app as c:
            response = c.get('/')
            data = json.loads(response.data)
            self.assertSequenceEqual( {'success':'hello world'}, data )

    def test_review_to_dict_method(self):
        review_info = {'item_author':'Jorge Luis Borges', 'item_title':'Labrynthes'}
        review1 = Review(**review_info)
        self.assertEqual(review_info['item_author'], review1.to_dict()['item_author'])
        self.assertEqual(review_info['item_title'], review1.to_dict()['item_title'])

    def test_reviews_are_persisted(self):
        review_info = {'item_author':'Jorge Luis Borges', 'item_title':'Labrynthes'}
        review1 = Review(**review_info)
        # set_trace()
        db.session.add(review1)
        db.session.commit()
        self.assertEqual(review_info['item_author'], db.session.query(Review).first().item_author)

