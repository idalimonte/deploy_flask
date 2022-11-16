from flask import render_template,redirect,request, session
from flask import flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.magazine import Magazine
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/success')
def success():
    if "user_id" not in session:
        return redirect('/logout')
    user = User.by_id(session["user_id"])
    print(session['user_id'])
    return render_template("dashboard.html", user=user, all_magazines = Magazine.get_all_magazines())


@app.route('/show/<int:id>')
def show(id):
    data = {
        "id":id,
        }
    magazine = Magazine.get_one_magazine(data)
    return render_template("show.html", magazine=magazine, user=User.show(data))


@app.route('/new')
def new_mag():
    return render_template("add.html")

@app.route('/add', methods = ['POST'])
def new_magazine():
    if not Magazine.validate_magazine(request.form):
        return redirect('/new')
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Magazine.add_magazine(data)
    return redirect('/success')

@app.route('/user/account')
def account_page():
    data = {
        'id': session['user_id']
    }
    user = User.get_user_mag(data)
    return render_template("edit.html", user=user, magazines= Magazine.get_all_magazines())

@app.route('/user/account/update', methods=["POST"])
def update():
    if not User.validate_update(request.form):
        return redirect('/user/account')
    User.update(request.form)
    return redirect('/success')

@app.route('/destroy/<int:id>')
def delete(id):
    data = {
        "id":id
    }
    Magazine.destroy(data)
    return redirect('/success')