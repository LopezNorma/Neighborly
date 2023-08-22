from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import helpme, user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.helpme import Helpme


@app.route('/dashboard')
def dashboard():
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id': session['logged_in_id']
    }
    return render_template('dashboard.html', all_helpmes=helpme.Helpme.s(), one_user=user_model.User.get_user_by_id(data))

#THIS ROUTE IS /NEW/HELPME is what wireframe 3 should be connected to. 
#When the user is logged in, and wants to create a new helpme, it will direct you to this.
#this form should be the title, description, location form on wireframe 3
#'new_helpme.html' can be named this or anything else - placeholder for now
@app.route('/new/helpme')
def helpme():
    if 'logged_in_id' not in session: 
        return redirect('/')
    data={
        'id': session['logged_in_id']
    }
    return render_template('new_helpme.html', one_user=user_model.User.get_user_by_id(data))


#create helpme - new helpme page - this route should match the html for creating a new job
@app.route('/helpme/create', methods=['POST'])
def create_job():
    if not helpme.Helpme.validate_helpme(request.form):
        return redirect('/new/helpme')
    helpme.Helpme.save_helpme

#read (show one specific helpme)
@app.route('/helpmes/show/<int:id>')
def show_helpme(id):
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id': id
    }
    return render_template('show_helpme.html', one_helpme=helpme.Helpme.get_helpme_by_id(data), one_helpme=helpme.Helpme.get_one_helpme(data))
    
@app.route('/helpmes/edit/<int:id>')
def edit_helpme(id):
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id': id
    }
    return render_template('edit_helpme.html', one_helpme=helpme.Helpme.get_one_helpme(data))

@app.route('/helpme/update', methods=['POST'])
def update_helpme():
    if not helpme.Helpme.validate_helpme(request.form):
        return redirect(f'/helpmes/edit/{request.form["id"]}')
    helpme.Helpme.update_sighting(request.form)
    return redirect(f'/sightings/show/{request.form["id"]}') #change this to dashboard once working

#delete
@app.route('/helpmes/delete', methods=['POST']) 
def delete_helpme():
    helpme.Helpme.delete_helpme(request.form)
    return redirect('/dashboard')