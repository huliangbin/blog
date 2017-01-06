# coding=utf-8

# only for debug

from app import app
from werkzeug.contrib.fixers import ProxyFix

app.secret_key = 'super secret key'
app.wsgi_app = ProxyFix(app.wsgi_app)

app.run(debug=True, port=5000)
