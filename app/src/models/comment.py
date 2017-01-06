# coding:utf8
from app import db
from app.src.models.user import User


class Comment(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_user = db.Column(db.Integer, index=True)
    blog = db.Column(db.Integer, index=True, nullable=False)  # 哪篇博客下的评论
    to_what = db.Column(db.Integer, index=True, default=0)  # 哪条评论下的评论
    to_who = db.Column(db.Integer, default=0)  # 回复谁
    context = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '%s, %s, %s' % (self.id, self.post_user, self.context)

    @property
    def post_nickname(self):
        record = User.query.filter_by(id=self.post_user).first()
        if not record:
            return ''
        return record.nickname

    @property
    def replys(self):
        record = Comment.query.filter_by(to_what=self.id).all()
        return record

    @property
    def replynickname(self):
        if self.to_who == 0:
            return ''
        record = User.query.filter_by(id=self.to_who).first()
        if record:
            return record.nickname
        return ''
