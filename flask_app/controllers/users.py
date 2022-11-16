from flask import render_template,redirect,request, session, flash
from flask_app import app
from ..models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/create', methods=["POST"])
def create():
    if not User.validate_user_reg(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.create_user(data)
    session['user_id'] = id
    return redirect ('/success')


@app.route('/login', methods=["POST"])
def login():
    user = User.by_email(request.form)
    if not user:
        flash("Email is invalid.", "login")
        return redirect('/home')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password is invalid", "login")
        return redirect('/home')
    session['user_id'] = user.id
    return redirect('/success')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')