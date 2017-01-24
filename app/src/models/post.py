# coding:utf8
import re

from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '%s, %s' % (self.id, self.title)

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def get_tags(self):
        return self.tags.split(',')

    @property
    def preview(self):
        content_preview = re.sub(r'</?\w+[^>]*>|&nbsp;', '', self.content)
        return content_preview[:100]
