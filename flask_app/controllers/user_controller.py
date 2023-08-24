from flask_app import app
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models import helpme
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def create():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    print('#############')
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']) 
    }
    print(data, '#' *20)
    # id = User.save(data)
    user_id = User.save(data)
    session['user_id'] = user_id
    # print(request.form)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    one_user = User.get_user_by_email(data)
    if not one_user:
        flash('Invalid email or password!!')
        return redirect('/')
    session ['user_id']= one_user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('logout')
    data = {
        'id': session ['user_id']
    }
    get_all_helpmes = helpme.Helpme.get_all_helpmes()
    return render_template('dashboard.html', user = User.get_by_id, get_all_helpmes = get_all_helpmes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')