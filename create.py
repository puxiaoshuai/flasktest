from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/flasktest'
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
        return "cate:%s" % self.name


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


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello,Java', "hahahahah,java", java, datetime.utcnow())
    file12 = File('Hello,Python', "fsdfsdf,python", python, datetime.utcnow())
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file12)
    db.session.commit()
    """ a=Category.query.filter_by(id=1).first()
    print(a.file.all())"""

    # app.run(port=3000)
