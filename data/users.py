
import hashlib
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    orders = orm.relationship("Orders", back_populates='user')


    def set_password(self, password:str):
        self.hashed_password = hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hashed_password == hashlib.md5(password.encode()).hexdigest()
    def __repr__(self):
        return f'{self.name} {self.email}'
