# coding:utf-8
from flask import render_template, request

from app import app
from app.src.models.post import Post


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    interval = 3
    count = Post.query.count()
    max_page = count // interval + (1 if count % interval > 0 else 0)
    max_page = 1 if max_page < 1 else max_page

    page = max(1, page)
    page = min(max_page, page)

    # 查询最近的文章
    posts = Post.query.filter(Post.temp == 1).order_by(Post.id.desc()).offset((page - 1) * interval).limit(interval)

    return render_template("index.html", title=u"主页", recent_posts=posts, querypage=page, max_page=max_page,
                           child_title=u"最新发布")


@app.route("/search", methods=['POST'])
def search():
    search_text = request.form['st']
    posts = Post.query.filter(
        Post.title.like('%' + search_text + '%') | Post.tags.like('%' + search_text + '%')).order_by(Post.id.desc())
    print posts
    return render_template("index.html", title=u"搜索结果", recent_posts=posts, querypage=1, max_page=1, child_title=u"搜索结果")
