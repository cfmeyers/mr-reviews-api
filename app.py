from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from sqlalchemy import func
from ipdb import set_trace

app = Flask(__name__)
cors = CORS(app)
db = SQLAlchemy(app)
app.config.from_object('config')



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
    genres = db.Column(db.Text)

    def to_dict(self):
        return {'id': self.id, 'author': self.author, 
                'item_title': self.item_title, 'item_author': self.item_author,
                'item_asin': self.item_asin, 'item_image_url': self.item_image_url,
                'post_url': self.post_url, 'date': self.date.__str__(), 'genres': self.genres }



@app.route('/')
def hello_world():
    return jsonify({'success':'hello world'})


@app.route('/api/v1/reviews', methods=['GET'])
def get_reviews():
    author = request.args.get('author') or ''
    title = request.args.get('title') or ''
    genre = request.args.get('genre') or ''

    query = (db.session.query(Review)
            .filter(Review.item_author.ilike('%'+author+'%'))
            .filter(Review.item_title.ilike('%'+title+'%'))
            .filter(Review.genres.ilike('%'+genre+'%'))
            )

    results = [result.to_dict() for result in query]
    # set_trace()
    return jsonify({'results':results})

if __name__ == '__main__':
    app.run()





