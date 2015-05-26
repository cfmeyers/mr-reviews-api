import unittest, json
from app import app, db, Review
from ipdb import set_trace


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/marginal-review-test'
        self.app = app.test_client()
        db.create_all()

        #fixtures
        self.review_fixtures = {
                'labrynthes' : {'item_author':'Jorge Luis Borges', 'item_title':'Labrynthes', 'genres':''},
                'ficciones' : {'item_author':'Jorge Luis Borges', 'item_title':'Ficciones','genres':''}, 
                'aleph' : {'item_author':'Jorge Luis Borges', 'item_title':'El Aleph','genres':''},
                'father brown' : {'item_author':'G.K. Chesterton', 'item_title':'Father Brown', 'genres':''}
                }

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_wired_up(self):
        with self.app as c:
            response = c.get('/')
            data = json.loads(response.data)
            self.assertSequenceEqual( {'success':'hello world'}, data )

    def test_review_to_dict_method(self):
        labrynthes = self.review_fixtures['labrynthes']
        review = Review(**labrynthes)
        self.assertEqual(labrynthes['item_author'], review.to_dict()['item_author'])
        self.assertEqual(labrynthes['item_title'], review.to_dict()['item_title'])

    def test_reviews_are_persisted(self):
        labrynthes = self.review_fixtures['labrynthes']
        db.session.add(Review(**labrynthes))
        db.session.commit()
        self.assertEqual(labrynthes['item_author'], db.session.query(Review).first().item_author)

    def test_reviews_author_param(self):
        borges_books = [self.review_fixtures['labrynthes'], self.review_fixtures['ficciones'], self.review_fixtures['aleph']]
        for key, book in self.review_fixtures.iteritems():
            db.session.add(Review(**book))
        db.session.commit()

        with self.app as c:
            response = c.get('/api/v1/reviews?author=Jorge%20Luis%20Borges')
            data = json.loads(response.data)
            self.assertItemsEqual( [d['item_title'] for d in borges_books], [d['item_title'] for d in data['results']] )

    def test_reviews_author_inexact_param(self):
        borges_books = [self.review_fixtures['labrynthes'], self.review_fixtures['ficciones'], self.review_fixtures['aleph']]
        for key, book in self.review_fixtures.iteritems():
            db.session.add(Review(**book))
        db.session.commit()

        with self.app as c:
            response = c.get('/api/v1/reviews?author=Borges')
            data = json.loads(response.data)
            self.assertItemsEqual( [d['item_title'] for d in borges_books], [d['item_title'] for d in data['results']] )

    def test_reviews_author_case_insensitive_param(self):
        borges_books = [self.review_fixtures['labrynthes'], self.review_fixtures['ficciones'], self.review_fixtures['aleph']]
        for key, book in self.review_fixtures.iteritems():
            db.session.add(Review(**book))
        db.session.commit()

        with self.app as c:
            response = c.get('/api/v1/reviews?author=borges')
            data = json.loads(response.data)
            self.assertItemsEqual( [d['item_title'] for d in borges_books], [d['item_title'] for d in data['results']] )

    def test_reviews_all(self):
        all_books = [self.review_fixtures['labrynthes'], self.review_fixtures['ficciones'], self.review_fixtures['aleph'], self.review_fixtures['father brown']]
        for key, book in self.review_fixtures.iteritems():
            db.session.add(Review(**book))
        db.session.commit()

        with self.app as c:
            response = c.get('/api/v1/reviews')
            data = json.loads(response.data)
            self.assertItemsEqual( [d['item_title'] for d in all_books], [d['item_title'] for d in data['results']] )

    def test_reviews_genre_param(self):

        for key, book in self.review_fixtures.iteritems():
            book_rev = Review(**book)
            if book_rev.item_author == 'Jorge Luis Borges':
                book_rev.genres += 'Wierd'
            else:
                book_rev.genres += 'Mystery'
            db.session.add(book_rev)

        db.session.commit()

        with self.app as c:
            response = c.get('/api/v1/reviews?genre=Mystery')
            data = json.loads(response.data)
            gk = db.session.query(Review)[3]
            self.assertItemsEqual( [self.review_fixtures['father brown']['item_title']], [d['item_title'] for d in data['results']] )





