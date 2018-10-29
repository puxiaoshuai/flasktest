from datetime import datetime
import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, abort
import json
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)
app.config["DEBUG"] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/flasktest'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:puhao@localhost/flasktest'
# ?????????????????????
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# ????????SQL??
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

client = MongoClient('127.0.0.1', 27017)
mongo = client.tags


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

    def __init__(self, title, content, category, create_time):
        self.title = title
        self.content = content
        self.create_time = create_time
        self.category = category

    def __repr__(self):
        return "file is%s" % self.title

    def add_tag(self, tag_name):
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']  # key{"file_id":1,"tags":[python]}
            if tag_name not in tags:
                tags.append(tag_name)
            mongo.files.update_one({'file_id': self.id}, {
                '$set': {'tags': tags}})
        else:
            tags = [tag_name]
            mongo.files.insert_one({'file_id': self.id, 'tags': tags})
        return tags

    def remove_tag(self, tag_name):
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            try:
                tags.remove(tag_name)
                new_tags = tags
            except ValueError:
                return tags
            mongo.files.update_one({'file_id': self.id}, {
                '$set': {'tags': new_tags}})
            return new_tags
        return []

    @property
    def tags(self):
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            return file_item['tags']
        else:
            return []


def insert_datas():
    java = Category('Java1')
    python = Category('Python1')
    file1 = File('Hello,Java1',
                 "I don't have any idea who originally wrote these utilities. If anybody does, please send some mail to noel@gnu.ai.mit.edu and I'll add your information here!",
                 java, datetime.now())
    file2 = File('Hello,Python1',
                  "A big thanks to Dirk for kicking me back into gear again after a long period of no work on this project.",
                  python, datetime.utcnow())
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    db.session.rollback()
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')



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
    '''db.drop_all()
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello,Java',
                 "I don't have any idea who originally wrote these utilities. If anybody does, please send some mail to noel@gnu.ai.mit.edu and I'll add your information here!",
                 java, datetime.now())
    file12 = File('Hello,Python',
                  "A big thanks to Dirk for kicking me back into gear again after a long period of no work on this project.",
                  python, datetime.utcnow())
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file12)
    db.session.commit()
    '''
    app.run(port=3000)
