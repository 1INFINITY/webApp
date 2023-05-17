from datetime import datetime
from flask_login import UserMixin

from application import db, manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password
        }
    def __repr__(self):
        return '<User %r>' % self.id

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    user_id = db.Column(db.ForeignKey(User.id))
    user = db.relationship(User, backref='users')

    comments = db.relationship('Comment', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'intro': self.intro,
            'text': self.text,
            'date': self.date,
            'user_id': self.user_id
        }
    def __repr__(self):
        return '<Article %r>' % self.id

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    user_id = db.Column(db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

    article_id = db.Column(db.ForeignKey(Article.id))

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'date': self.date,
            'user_id': self.user_id,
            'article_id': self.article_id
        }
    def __repr__(self):
        return '<Comment %r>' % self.id
@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
