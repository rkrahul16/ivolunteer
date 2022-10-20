from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_required, current_user
from models import availableform, User, timeentryform
from app import create_app, db
from datetime import datetime

data1=[{'type': 'POV'}, {'type': 'RFP'}, {'type': 'Hiring'}, {'type': 'Accelerator'}, 
            {'type': 'Knowledge Sharing'}, {'type': 'Team Building Activities'}, 
            {'type': 'LXT'}, {'type': 'Others'}]
data2=[{'involvement': 'shadow'}, {'involvement': 'own'}]
# our main blueprint
main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def home():
    return render_template('index.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/availability',methods=['GET', 'POST']) # availability page 
@login_required
def availability():
    if request.method=='GET': # If the request is GET we return the form
        return render_template('availability_form.html', involvement=data2, typeofwork=data1)
    else: # if the request is POST, fill the form and store it to DB
        startdate = datetime.strptime(request.form.get('startdate'),'%Y-%m-%d')
        enddate = datetime.strptime(request.form.get('enddate'),'%Y-%m-%d')
        avail_hours = request.form.get('avail_hours')
        interest = request.form.get('interest')
        involvement = request.form.get('involvement')
        typeofwork = request.form.get('typeofwork')
        # Update the table with new entry
        new_entry = availableform(startdate=startdate, 
                                  enddate=enddate, 
                                  avail_hours=avail_hours,
                                  interest=interest, 
                                  involvement=involvement,
                                  typeofwork=typeofwork)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('main.profile'))

@main.route('/timeEntry',methods=['GET', 'POST']) # timeEntry page 
@login_required
def timeentry():
    if request.method=='GET': # If the request is GET we return the form
        return render_template('updatetime_form.html', involvement=data2, typeofwork=data1)
    else: # if the request is POST, fill the form and store it to DB
        startdate = datetime.strptime(request.form.get('startdate'),'%Y-%m-%d')
        enddate = datetime.strptime(request.form.get('enddate'),'%Y-%m-%d')
        hours_spent = request.form.get('hours_spent')
        involvement = request.form.get('involvement')
        typeofwork = request.form.get('typeofwork')
        project = request.form.get('project')
        owner = request.form.get('owner')
        name=current_user.name
        email=current_user.email
        #Update the table with new entry
        new_entry = timeentryform(startdate=startdate, 
                                  enddate=enddate, 
                                  hours_spent=hours_spent,
                                  project=project, 
                                  owner=owner, 
                                  involvement=involvement,
                                  typeofwork=typeofwork,
                                  name=name,
                                  email=email)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('main.profile'))

@main.route('/users') # profile page that return 'profile'
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@main.route('/timesheet') # profile page that return 'profile'
@login_required
def timesheet():
    timeentry = timeentryform.query.filter_by(email= current_user.email).all()
    return render_template('timesheet.html', timeentry=timeentry)

@main.route('/resources', methods=['GET', 'POST']) # profile page that return 'profile'
@login_required
def resources():
    if request.method=='GET': # If the request is GET we return the form
        return render_template('resource_search_form.html', typeofwork=data1)
    else: # if the request is POST, fill the form and store it to DB
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        typeofwork = request.form.get('typeofwork')
        print(type(startdate))
        startdate_obj= datetime.strptime(startdate, '%Y-%m-%d')
        print(startdate_obj)
        avail_resource = availableform.query.filter_by(startdate>=startdate_obj).all()
        return render_template('availableResourceList.html', avail_resource=avail_resource)
app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    #db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True, host="0.0.0.0") # run the flask app on debug mode
