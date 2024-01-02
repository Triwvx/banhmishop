from flask import session, render_template, redirect, request
from flask_app import app
from flask_app.models.user_models import User
from flask_app.models.order_models import Order
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

# *** IF user is not logged in- cannot get to any of the routes *** 

## home page / login / register ### 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def loggingin():
    return render_template("registration_login.html")

@app.route('/register',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Not a valid Email! Try again","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Incorrect Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

## dashboard ## 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data) ,order=Order.get_everything())

## Menu ## 
@app.route('/menu')
def menu():
    return render_template ('menu.html')

## view cart ##
@app.route('/view-cart')
def cart():
    return render_template ('cart.html')

## Edit User ## 
@app.route("/edit_user/<int:id>")
def show_edit_user_page(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        'id':id
    }
    return render_template("account.html", users=User.get_by_id(data))

@app.route ("/edit_user/<int:id>", methods=["POST"])
def show_user_account(id):
    if 'user_id' not in session:
        return redirect ("/")
    if not User.validate_register(request.form):
        return redirect("/edit_user/<int:id>")
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    return redirect ("/dashboard", users=User.edit_user(data), magazines=Magazine.get_user_with_magazine())

## logout and delete ## 
@app.route("/logout")
def logout():
    session.clear()
    return redirect ('/')



