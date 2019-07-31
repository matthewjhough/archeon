from src.common.db import db

relationship = db.relationship
Column = db.Column
Integer = db.Integer
Model = db.Model
String = db.String
ForeignKey = db.ForeignKey
Text = db.Text
Table = db.Table
backref = db.backref

user_session_table = Table('user_session', Model.metadata,
                           Column('user_id', Integer, ForeignKey('users.uuid')),
                           Column('session_id', Integer, ForeignKey('sessions.uuid'))
                           )
