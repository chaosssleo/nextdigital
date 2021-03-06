from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    newsposts = db.relationship('newsPost', backref='author', lazy='dynamic')
    movenewsPost = db.relationship('movenewsPost', backref='author', lazy='dynamic')
    onearticlePost = db.relationship('onearticlePost', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class newsPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posttitle = db.Column(db.String(50))
    body = db.Column(db.String(140))
    cover_name = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<newsPost {}>'.format(self.body)


class movenewsPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posttitle = db.Column(db.String(50))
    body = db.Column(db.String(140))
    cover_name = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<movenewsPost {}>'.format(self.body)


class onearticlePost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posttitle = db.Column(db.String(50))
    body = db.Column(db.String(140))
    cover_name = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<onearticlePost {}>'.format(self.body)


class base_navigation(db.Model):
    page_name = db.Column(db.String(20), primary_key=True)
    page_link = db.Column(db.String(100))

    def __repr__(self):
        return '<Base_navigation {}>'.format(self.page_name)


class apple_daily_navigation(db.Model):
    page_name = db.Column(db.String(20), primary_key=True)
    page_link = db.Column(db.String(100))

    def __repr__(self):
        return '<apple_daily_navigation {}>'.format(self.page_name)


class move_news_navigation(db.Model):
    page_name = db.Column(db.String(20), primary_key=True)
    page_link = db.Column(db.String(100))

    def __repr__(self):
        return '<move_news_navigation {}>'.format(self.page_name)


class one_article_navigation(db.Model):
    page_name = db.Column(db.String(20), primary_key=True)
    page_link = db.Column(db.String(100))

    def __repr__(self):
        return '<one_article_navigation {}>'.format(self.page_name)