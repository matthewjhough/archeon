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

user_session_table = Table('user_session', Model.metadata,
                           Column('user_id', Integer, ForeignKey('users.id')),
                           Column('session_id', Integer, ForeignKey('sessions.id'))
                           )


class User(Model):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(256), index=True, unique=True)

	# one to many
	messages = relationship('Message', backref='user')

	def __repr__(self):
		return '<User %r>' % self.username


class Session(Model):
	__tablename__ = 'sessions'
	id = Column(Integer, primary_key=True)

	# one to many
	messages = relationship('Message', backref='session')

	# many to many
	users = relationship('User', secondary=user_session_table, backref=db.backref('sessions', lazy='dynamic'))

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
