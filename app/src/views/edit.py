# coding:utf-8
import os
import uuid

from flask import g, jsonify
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import secure_filename

from app import app, db
from app.src.models.comment import Comment
from app.src.models.post import Post


@app.route('/edit')
def edit():
    user = g.user
    if user is None or not user.is_authenticated:
        return render_template('404.html'), 404
    if not user.is_admin:
        return render_template('404.html'), 404
    return render_template("edit.html", title=u"编辑")


@app.route('/post', methods=['POST'])
def post():
    user = g.user
    if user is None or not user.is_authenticated:
        return render_template('404.html'), 404
    if not user.is_admin:
        return render_template('404.html'), 404
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tags[]')

    new_post = Post(title=title, content=content, tags=','.join(tags))
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'rd': url_for('blog', blog_id=new_post.id)})


@app.route('/blog/<int:blog_id>', methods=['POST', 'GET'])
def blog(blog_id):
    record = Post.query.filter_by(id=blog_id).first()
    blog_comment = Comment.query.filter_by(blog=blog_id, to_what=0).all()
    if not record:
        return render_template('500.html'), 500
    return render_template('blog.html',
                           record=record,
                           blog_comment=blog_comment)


@app.route('/comment', methods=['POST'])
def comment():
    user = g.user
    if user is None or not user.is_authenticated:
        return render_template('404.html'), 404
    context = request.form['context']
    blog_id = request.form['bid']
    new_comment = Comment(post_user=g.user.id, blog=blog_id, context=context)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/reply', methods=['POST'])
def comment2someone():
    user = g.user
    if user is None or not user.is_authenticated:
        return render_template('404.html'), 404
    context = request.form['context']
    blog_id = request.form['bid']
    to_what = request.form['to_what']
    to_who = request.form['to_who']
    new_comment = Comment(post_user=g.user.id, blog=blog_id,
                          context=context, to_what=to_what, to_who=to_who)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        image_upload = request.files['fileup']
        if image_upload:
            image_type = image_upload.content_type.split('/')[1]
            filename = '.'.join([str(uuid.uuid1()), image_type])
            image_upload.save(os.path.join(app.config['UPLOAD_PATH'] + app.config['IMAGE_DIR'], filename))
            img_path = "/" + app.config['IMAGE_DIR'] + filename
            return jsonify({'url': img_path})
    return jsonify({'error': '上传失败'})
