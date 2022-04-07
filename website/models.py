from email.policy import default
from time import timezone   #import timezone 
from . import db    #import database
from flask_login import UserMixin
from sqlalchemy.sql import func #fungsi untuk memberikan waktu sekarang




#table user atau table tAnggota
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    Jurusan = db.Column(db.String(150))
    booksborrow=db.relationship('Bookborrow')
    bookreturn=db.relationship('Bookreturn')
    def __repr__(self):
        return f"User('{self.nim}'"

#table books atau table tBuku
class Books(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    bookName=db.Column(db.String(150), unique=True, nullable=False)
    bookCount=db.Column(db.Integer, nullable=False)
    bookAuthor=db.Column(db.String(150), nullable=False)
    
    bookreturn=db.relationship('Bookreturn')
    Bookborrow=db.relationship('Bookborrow')
    
    def __repr__(self):
        return f"Uploaded('{self.bookName}', '{self.bookAuthor}', '{self.bookCount}')"
    
#table Bookborrow atau table tPinjam
class Bookborrow(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    bookId=db.Column(db.Integer, db.ForeignKey('books.id'))
    userId=db.Column(db.Integer, db.ForeignKey('user.id'))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    
    def __repr__(self):
        return f"Uploaded('{self.bookId}', '{self.userId}')"
    
    
#table Bookreturn atau table tKembali
class Bookreturn(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    bookId=db.Column(db.Integer, db.ForeignKey('books.id'))
    userId=db.Column(db.Integer, db.ForeignKey('user.id'))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    

    def __repr__(self):
        return f"Uploaded('{self.bookId}', '{self.userId}')"