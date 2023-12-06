# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String , nullable = False)
    email = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    
    borrows = db.relationship('Borrow', backref='user') 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    genre = db.Column(db.String, nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    
    author = db.relationship('Author')
    borrows = db.relationship('Borrow', backref='book')
    
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    biography = db.Column(db.Text)
    
class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    checkout_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date )


