from src.common.db import db
from src.common.model import user_session_table

relationship = db.relationship
Column = db.Column
Integer = db.Integer
Model = db.Model
String = db.String
ForeignKey = db.ForeignKey
Text = db.Text
Table = db.Table
backref = db.backref


class SessionModel(Model):
	__tablename__ = 'sessions'
	uuid = Column(Integer, primary_key=True)

	# one to many
	messages = relationship('MessageModel', backref='session')

	# many to many
	users = relationship('UserModel', secondary=user_session_table, backref=db.backref('sessions', lazy='dynamic'))

	def __repr__(self):
		return '<session %r>' % self.id
