from quanta_quire.extensions import db
from datetime import datetime


class ChatLog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)
  user = db.Column(db.String)
  question = db.Column(db.Text)
  answer = db.Column(db.Text)
  point = db.Column(db.Integer, default=None)
