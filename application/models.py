from datetime import datetime
from flask_login import UserMixin

from application import db, manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
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
    def __repr__(self):
        return '<Article %r>' % self.id


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
