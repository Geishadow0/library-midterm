from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import Bookborrow, Bookreturn, Books,  User
from . import db

#inisialisasi blueprint
views = Blueprint('views', __name__)

#main root website
@views.route('/' , methods=['GET', 'POST'])
@login_required
def home():

    #menambahkan buku
    if request.method == 'POST':
        Bname = request.form.get('name')
        Bauthor = request.form.get('author')
        Bcount = request.form.get('count')

        #membuat agar tidak ada buku yang sama tercatat secara tidak sengaja
        book = Books.query.filter_by(bookName=Bname).first()
        if book:
            flash('Book already exist', category='error')
        else:
            #menambahkan entry pada database
            new_book = Books(bookName=Bname, bookAuthor=Bauthor, bookCount=Bcount)
            db.session.add(new_book)
            db.session.commit()
            flash('Books Added', category='success')
    
    
            
            
    #menampilkan html
    return render_template("home.html", user=current_user, container=Books.query.all())



#method menghapus buku
@views.route('/delete/<id>', methods=['GET','POST'])
def delete_book(id):
    books=Books.query.filter_by(id=id).first()
    db.session.delete(books)
    db.session.commit()
    flash('Books Deleted')
    return redirect(url_for('views.home'))

#method meminjam
@views.route('/borrow/<id>', methods=['POST', 'GET'])
def borrow(id):

    books=Books.query.filter_by(id=id).first()
    #stok buku dikurangi
    books.bookCount-=1
    new_borrow = Bookborrow(bookId=id, userId=current_user.id)
    db.session.add(new_borrow)
    db.session.commit()
    flash('Books Borrowed', category='success')
    return redirect(url_for('views.home'))
    
#method mengembalikan buku
@views.route('/bookreturn/<id>', methods=['POST', 'GET'])
def bookreturn(id):
    books=Books.query.filter_by(id=id).first()
    #stock buku ditambah
    books.bookCount+=1
    new_return = Bookreturn(bookId=id, userId=current_user.id)
    db.session.add(new_return)
    db.session.commit()
    flash('Books Returned', category='success')
    return redirect(url_for('views.home'))

#route untuk ke halaman log
@views.route('/log', methods=['GET', 'POST'])
def log():
    #data untuk table pinjam dan kembalikan di panggil dan disimpan dalam container
    container=Bookborrow.query.all()
    container2=Bookreturn.query.all()
    
    return render_template("log.html",user=current_user, container=container, container2=container2)
    