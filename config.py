import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:www.4399.com@119.23.252.15:3316/live_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qwertyuiop'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SUBJECT_PREFIX = ['Parkhai']
    MAIL_SENDER = 'Parkhai Admin <parkhai@parkhai.club>'
    MAIL_ADMIN = os.environ.get('FLASKY_ADMIN') or 'parkhai'
    ROOMS_PER_PAGE = 20
