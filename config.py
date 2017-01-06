# coding:utf-8
import os
import re

WTF_CSRF_ENABLED = True
SECRET_KEY = '\xf4=7\x11X;\x03x\xb0\xe3\xd3\x14\xef\xe5\xad;\xf3p\xa0\xd1]\xa3\x7f)'

print SECRET_KEY
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql://hlb:hlb@127.0.0.1:3306/myblog?charset=utf8'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_PATH = os.path.join(basedir, 'app/static/')
IMAGE_DIR = 'img/'
filter = []
