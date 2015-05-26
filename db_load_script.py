from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Link, Book, Genre, Base

import os, re, time

engine = create_engine('sqlite:///mr_posts.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
genres = session.query(Genre).all()
books = session.query(Book).all()

from app import app, db, Review
from app import Genre as DeployedGenre

for book in books:
    asin = re.search(r"[\dA-Z]{10}", book.link.href).group()
    post_author = book.link.post.author
    post_url = book.link.post.url
    new_review = Review(item_title=book.title[:249], 
            item_author=book.author, 
            item_image_url=book.image_url, 
            item_asin=asin, 
            author=post_author,
            post_url=post_url,
            date=book.link.post.date)
    for genre in book.genres:
        deployed_genre = db.session.query(DeployedGenre).filter(DeployedGenre.name==genre.name).first()
        if not deployed_genre:
            deployed_genre = DeployedGenre(genre.name)
            db.session.add(deployed_genre)
            print deployed_genre.name
        else:
            print "FOUND"*30
        new_review.genres.append(deployed_genre)
    db.session.add(new_review)

db.session.commit()
# dg = db.session.query(DeployedGenre).all()
# for g in dg:
#     print g.name


    # genres = relationship('Genre', secondary=association_table, backref='reviews')


# for genre in genres:
#     db.session.add(DeployedGenre(genre.name))

# db.session.commit()


