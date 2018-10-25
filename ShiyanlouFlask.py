from datetime import datetime
import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, abort
import json

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)
app.config["DEBUG"] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/flasktest'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:puhao@localhost/flasktest'
# ?????????????????????
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# ????????SQL??
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "%s" % self.name


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    create_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category', backref=db.backref('file', lazy='dynamic'))

    def __init__(self, title, content, category, create_time=None):
        self.title = title
        self.content = content
        if create_time is None:
            self.create_time = datetime.utcnow()
        self.category = category

    def __repr__(self):
        return "file is%s" % self.title
    def add_tag(self,tag_name):
        pass
    def remove_tag(self,tag_name):
        pass
    @property
    def tags(self):
        pass


@app.route('/')
def index():
    # db
    files = File.query.all()
    print(files)
    return render_template('index.html', data=files)


@app.route("/files/<fileid>")
def file(fileid):
    data = {}
    files = File.query.filter_by(id=fileid).all()

    if len(files) == 0:
        abort(404)
    else:
        data['content'] = files[0].content
        data['time'] = files[0].create_time
        data['cate'] = files[0].category
    return render_template('file.html', data=data)



@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello,Java', "I don't have any idea who originally wrote these utilities. If anybody does, please send some mail to noel@gnu.ai.mit.edu and I'll add your information here!", java, datetime.now())
    file12 = File('Hello,Python', "A big thanks to Dirk for kicking me back into gear again after a long period of no work on this project.", python, datetime.utcnow())
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file12)
    db.session.commit()
    app.run(port=3000)
