from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from kozha import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
# ABOUT UserMixin
# has an is_authenticated() method that returns True if the user has provided valid credentials
# has an is_active() method that returns True if the user’s account is active
# has an is_anonymous() method that returns True if the current user is an anonymous user
# has a get_id() method which, given a User instance, returns the unique ID for that object
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable = False, default='dummy.jpg')
    password = db.Column(db.String(60), nullable=False)
    style = db.Column(db.String(30), nullable=False, default='베이직')
    posts = db.relationship('Post', backref='author', lazy=True)
    profile = db.Column(db.Text(), default='User Profile')

    def get_reset_token(self,expires_sec=1800): # 보안을 위해 정보수정시 보안키가 유효한 시간설정
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
    # repr은 전달받은 값으 고유 메모리주솔를 반환하는 메소드이며 __repr__을 통하여 전달받은 값을 우리가 이해할 수 있는 표현으로 바꿔서 리턴해준다.
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.style}')"


# POST 테이블과 Hashtag테이블 사이에 m:n 관계를 형성해주기 위해 tags를 작성
tags = db.Table('tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id'), primary_key=True)
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    style = db.Column(db.String(30), nullable=False, default='베이직')
    tags = db.relationship('Hashtag', secondary=tags, backref=db.backref('tagging', lazy='dynamic'))
    content_img = db.Column(db.String(20), nullable=False, default='dummy_post.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}','{self.content_img}','{self.tags}')"


class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(20), nullable = False)