# 若存在migrate_version表，会执行失败！报DatabaseAlreadyControlledError错误
from migrate.versioning import api
import os
from app.models import db


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:www.4399.com@119.23.252.15:3316/live_dev'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')

# db.drop_all()
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

print('create successed')
