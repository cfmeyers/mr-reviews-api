from flask import Flask, jsonify

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
# db = SQLAlchemy(app)
# Base = declarative_base()

# ####################################################################
# association_table = Table('association', Base.metadata,
#     Column('review_id', Integer, ForeignKey('review.id')), #left
#     Column('genre_id', Integer, ForeignKey('genre.id')) #right
# )
# ####################################################################


# class Review(Base):
#     """
#     author, item_title, item_author, item_asin, item_image_url, post_url, date fields
#     also genres, a many-to-many association table with Genre
#     """

#     __tablename__ = 'review'
#     id = db.Column(db.Integer, primary_key=True)
#     author = db.Column(db.String(250))
#     item_title = db.Column(db.String(250))
#     item_author = db.Column(db.String(250))
#     item_asin = db.Column(db.String(50))
#     item_image_url = db.Column(db.String(250))
#     post_url = db.Column(db.String(250))
#     date = Column(Date)
#     genres = relationship('Genre', secondary=association_table, backref='reviews')

#     def to_dict(self):
#         return {'id': self.id, 'author': self.author, 
#                 'item_title': self.item_title, 'item_author': self.item_author,
#                 'item_asin': self.item_asin, 'item_image_url': self.item_image_url,
#                 'post_url': self.post_url, 'date': self.date, 'genres': self.genres }


# ####################################################################
# class Genre(Base):

#     __tablename__ = 'genre'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120))

#     def __init__(self, name):
#         self.name = name


# ####################################################################


@app.route('/')
def hello_world():
    return jsonify({'success':'hello world'})

