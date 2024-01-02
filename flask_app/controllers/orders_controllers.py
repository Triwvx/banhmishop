from flask import flash
from flask import session, render_template, redirect, request
from flask_app import app
from flask_app.models.order_models import Order
from flask_app.models.user_models import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# *** IF user is not logged in- cannot get to any of the routes ***

# creating painting ##
@app.route("/magazines/new")
def create_new_magazine():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("add_magazine.html")


@app. route("/magazines/new", methods=["POST"])
def posting_new_magazine():
    if 'user_id' not in session:
        return redirect("/")
    if not Magazine.validate_magazine(request.form):
        return redirect("/magazines/new")
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    magazines=Magazine.save(data)
    return redirect('/dashboard')

## showing magazine info ##
@app.route("/show_magazine/<int:id>")
def show_magazine_info(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        'id': id
    }
    return render_template("show_magazine.html", magazine=Magazine.get_magazine_by_id(data))

## deleting a magazine ##
@app.route("/delete/<int:id>")
def delete_magazine(id):
    if 'user_id' not in session:
        return redirect("/")
    Magazine.delete_magazine(id)
    return redirect("/dashboard")

