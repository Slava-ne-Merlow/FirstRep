
import hashlib
import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Forwarders(SqlAlchemyBase, UserMixin):
    __tablename__ = 'forwarders'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    company = sqlalchemy.Column(sqlalchemy.String, nullable=True)


    def set_password(self, password:str):
        self.hashed_password = hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hashed_password == hashlib.md5(password.encode()).hexdigest()
    def __repr__(self):
        return f'{self.company} {self.name} {self.email}'
