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


class MessageModel(Model):
	__tablename__ = 'messages'
	uuid = Column(Integer, primary_key=True)
	content = Column(Text, index=True)

	# one to many
	user_id = Column(
		Integer, ForeignKey('users.uuid'))

	# many to many
	session_id = Column(
		Integer, ForeignKey('sessions.uuid')
	)

	def __repr__(self):
		return '<message %r>' % self.content
