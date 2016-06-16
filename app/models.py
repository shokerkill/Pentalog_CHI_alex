from app import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association = db.Table('association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('advice_id', db.Integer, db.ForeignKey('advices.id'))
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    advices = db.relationship('Advice',
                    secondary= association,
                    back_populates="victims")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Advice(db.Model):
    __tablename__ = 'advices'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(140))
    foreign_id = db.Column(db.Integer, unique=True)
    victims = db.relationship('User',
        secondary= association,
        back_populates="advices")

    def __repr__(self):
        return '<Post %r>' % (self.text)

