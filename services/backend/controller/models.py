# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    web_id = db.Column(db.Integer)
    question_text = db.Column(db.String(1023))
    answer = db.Column(db.String(255))
    publication_date = db.Column(db.Date)
