from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import helpme, user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# @app.route('/dashboard')
# def dashboard():
#     if 'logged_in_id' not in session:
#         return redirect('/')
#     data={
#         'id': session['logged_in_id']
#     }
#     get_all_helpmes = helpme.Helpme.get_all_helpmes()
#     return render_template('dashboard.html', get_all_helpmes = get_all_helpmes, one_user=user_model.User.get_user_by_id(data))

#THIS ROUTE IS /NEW/HELPME is what wireframe 3 should be connected to. 
#When the user is logged in, and wants to create a new helpme, it will direct you to this.
#this form should be the title, description, location form on wireframe 3
#'new_helpme.html' can be named this or anything else - placeholder for now
@app.route('/new/helpme')
def newhelpme():
    if 'user_id' not in session: 
        return redirect('/')
    data={
        'id': session['user_id']
    }
    return render_template('new.html', id = data['id'])


#create helpme - new helpme page - this route should match the html for creating a new job
@app.route('/helpme/create', methods=['POST'])
def create_job():
    if not helpme.Helpme.validate_helpme(request.form):
        return redirect('/new/helpme')
    data = {
        "title": request.form['title'],
        "location":request.form['location'],
        "description": request.form['description'],
        "user_id": request.form['user_id']
    }
    helpme.Helpme.save_helpme(data)
    return redirect('/dashboard')

#read (show one specific helpme)
@app.route('/helpmes/show/<int:id>')
def show_helpme(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': id
    }
    return render_template('check.html', one_helpme=helpme.Helpme.get_one_helpme(data))
    
@app.route('/helpmes/edit/<int:id>')
def edit_helpme(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': id
    }
    return render_template('edit.html', one_helpme=helpme.Helpme.get_one_helpme(data))

@app.route('/helpme/update/<int:id>', methods=['POST'])
def update_helpmes(id):
    if not helpme.Helpme.validate_helpme(request.form):
        return redirect(f'/helpmes/edit/'+id)    
    data = {
        "id": id,
        "title": request.form['title'],
        "location":request.form['location'],
        "description": request.form['description'],
        "user_id": session["user_id"]
    }
    helpme.Helpme.update_helpme(data)
    return redirect('/dashboard') #change this to dashboard once working

#delete
@app.route('/helpmes/delete/<int:id>') 
def delete(id):
    helpme.Helpme.delete_helpme(id)
    return redirect('/dashboard')

