import os

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/marginal-review'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
