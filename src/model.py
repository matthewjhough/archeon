from src.db import db

relationship = db.relationship
Column = db.Column
Integer = db.Integer
Model = db.Model
String = db.String
ForeignKey = db.ForeignKey
Text = db.Text
Table = db.Table
backref = db.backref


class User(Model):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(256), index=True, unique=True)
	session_id = Column(Integer, ForeignKey('sessions.id'))

	# one to many
	messages = relationship('Message', backref='user')

	def __repr__(self):
		return '<User %r>' % self.username


class Session(Model):
	__tablename__ = 'sessions'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))

	# one to many
	messages = relationship('Message', backref='session')

	def __repr__(self):
		return '<Session %r>' % self.id


class Message(Model):
	__tablename__ = 'messages'
	id = Column(Integer, primary_key=True)
	content = Column(Text, index=True)

	# one to many
	user_id = Column(
		Integer, ForeignKey('users.id'))

	# many to many
	session_id = Column(
		Integer, ForeignKey('sessions.id')
	)

	def __repr__(self):
		return '<Message %r>' % self.content
