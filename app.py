from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import func
from ipdb import set_trace

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')

####################################################################
association_table = db.Table('association', db.Model.metadata,
    db.Column('review_id', db.Integer, db.ForeignKey('review.id')), #left
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')) #right
)
####################################################################


class Review(db.Model):
    """
    author, item_title, item_author, item_asin, item_image_url, post_url, date fields
    also genres, a many-to-many association table with Genre
    """

    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), index=True)
    item_title = db.Column(db.String(250), index=True)
    item_author = db.Column(db.String(250), index=True)
    item_asin = db.Column(db.String(50))
    item_image_url = db.Column(db.String(250))
    post_url = db.Column(db.String(250))
    date = db.Column(db.Date)
    genres = relationship('Genre', secondary=association_table, backref='reviews')

    def to_dict(self):
        return {'id': self.id, 'author': self.author, 
                'item_title': self.item_title, 'item_author': self.item_author,
                'item_asin': self.item_asin, 'item_image_url': self.item_image_url,
                'post_url': self.post_url, 'date': self.date, 'genres': [g.name for g in self.genres] }


####################################################################
class Genre(db.Model):

    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)

    def __init__(self, name):
        self.name = name


####################################################################


@app.route('/')
def hello_world():
    return jsonify({'success':'hello world'})


@app.route('/api/v1/reviews')
def get_reviews():
    author = request.args.get('author') or ''
    title = request.args.get('title') or ''
    genre_name = request.args.get('genre') or ''

    if genre_name:
        genre = db.session.query(Genre).filter(Genre.name==genre_name)

    query = (db.session.query(Review)
            .filter(Review.item_author.ilike('%'+author+'%'))
            .filter(Review.item_title.ilike('%'+title+'%'))
            )
    if genre_name:
        query = query.filter(Review.genres.any(Genre.name==genre_name))

    results = [result.to_dict() for result in query]
    return jsonify({'results':results})





