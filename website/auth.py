from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#initialisasi blueprint
auth = Blueprint('auth', __name__)

#menghandle login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nim = request.form.get('nim')
        password = request.form.get('password')
        user = User.query.filter_by(nim=nim).first()
        if user:
            #mengecheck password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('nim does not exist.', category='error')
    #meredirrect ke halaman utama
    return render_template("login.html", user=current_user)

#menghandle logout
@auth.route('/logout')
@login_required
def logout():
    #funsi logout
    logout_user()
    #redirrect ke halaman login
    return redirect(url_for('auth.login'))

#menghandle sign up
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        nim = request.form.get('nim')
        Jurusan = request.form.get('Jurusan')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(nim=nim).first()
        #memfilter inputan yang tidak sesuai
        if user:
            flash('nim already exists.', category='error')
        elif len(nim) < 4:
            flash('nim must be greater than 3 characters.', category='error')
        elif len(Jurusan) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #password di hash dengan cara sha256
            new_user = User(nim=nim, Jurusan=Jurusan, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    #redirrect ke halaman utama
    return render_template("sign_up.html", user=current_user)
