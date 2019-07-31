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


class UserModel(Model):
	__tablename__ = 'users'
	uuid = Column(Integer, primary_key=True)
	username = Column(String(256), index=True, unique=True)

	# one to many
	messages = relationship('MessageModel', backref='user')

	def __repr__(self):
		return '<user %r>' % self.username
