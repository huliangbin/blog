from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    nickname = db.Column(db.String(255), index=True, unique=True)
    pwd = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(), default=False)
    avatar_url = db.Column(db.String(64), default='default-avatar')
    like = db.Column(db.String(1024), default='')
    comment = db.Column(db.String(1024), default='')

    def __repr__(self):
        return '%s, %s' % (self.id, self.nickname)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
