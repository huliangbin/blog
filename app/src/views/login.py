# coding:utf-8
import hashlib
from flask import g, jsonify
from flask import redirect
from flask import request
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import logout_user

from app import app, lm, db
from app.src.models.user import User
from config import filter


@app.route("/login", methods=['POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    username = request.form['un']
    password = request.form['pw']
    record = User.query.filter_by(username=username).first()
    if record is None:
        return jsonify({'error': '用户不存在'})
    md5 = hashlib.md5()
    md5.update(password)
    if record.pwd != md5.hexdigest():
        return jsonify({'error': '密码不正确'})
    login_user(record, remember=True)
    return redirect(url_for('index'))


@app.route("/register", methods=['POST'])
def register():
    username = request.form['un']
    nickname = request.form['ni']
    # 用户名是否重复
    old_record = User.query.filter_by(username=username).first()
    if old_record:
        return jsonify({'error': '用户名已存在'})

    if filter:
        for pattern in filter:
            if pattern.match(nickname):
                return jsonify({'error': '非法字符'})

    # md5加密密码
    password = request.form['pw']
    md5 = hashlib.md5()
    md5.update(password)

    new_user = User(username=username, nickname=nickname, pwd=md5.hexdigest())

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=True)
    return redirect(url_for('index'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user


@app.route("/rgc", methods=['POST'])
def register_check():
    username = request.form['un']
    old_record = User.query.filter_by(username=username).first()
    if old_record:
        return jsonify({'valid': False})
    else:
        return jsonify({'valid': True})


@app.route("/rgc_nickname", methods=['POST'])
def register_check_nickname():
    nickname = request.form['nickname']
    old_record = User.query.filter_by(nickname=nickname).first()
    if old_record:
        return jsonify({'valid': False})
    else:
        return jsonify({'valid': True})
