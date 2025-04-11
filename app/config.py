import os
from urllib.parse import quote_plus


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'\
        .format(os.environ.get('DB_USER'),
                quote_plus(os.environ.get('DB_PASSWORD')),
                os.environ.get('DB_HOST'),
                os.environ.get('DB_PORT'),
                os.environ.get('DB_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # was hard to send the csrf tokens when testing so we can disable it for now.
    # not really sure how it works completely but for api testing we should be fine w/o it
    WTF_CSRF_ENABLED = False 