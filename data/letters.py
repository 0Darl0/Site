import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Letters(SqlAlchemyBase):
    __tablename__ = 'letters'

    id = sqlalchemy.Column(sqlalchemy.BigInteger,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    who_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    topic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_delete = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user = orm.relationship('User', secondary="association", backref="news")
    # who = orm.relationship('User', back_populates='letters', foreign_keys="[Letters.who_id]")
