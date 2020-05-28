import os

from flask import render_template, url_for, redirect, flash, session

from application import app, bcrypt, Session
from application.forms import researchScholarsForm, loginForm, addProjects
from application.connection import collection, db
from application.scholars import scholarsList
Session(app)


def save_picture(form_picture, name):
    random_hex = name
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fname = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/users', picture_fname)
    form_picture.save(picture_path)

    return picture_fname


@app.route('/', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = loginForm()
    fetch_record = collection.find_one({"cust_id": 12345678})

    if session.get('username') == None:
        session['username'] = None

    if form.validate_on_submit():
        user = collection.find_one({"username": form.username.data})
        if user:
            if collection.find_one({'password': form.password.data}):
                flash(f'Welcome {user["name"]}', 'success')
                session['username'] = form.username.data
            else:
                flash('Please enter a correct password', 'danger')
        else:
            flash(f'No such username {form.username.data} exists', 'danger')


    scholarsList = fetch_record['scholars']
    return render_template('home.html', scholarsList=scholarsList, form=form, username=session['username'])


@app.route("/addscholars", methods=['GET', 'POST'])
def addScholars():
    if session.get('username') == None:
        session['username'] = None
    form = loginForm()
    ScholarsForm = researchScholarsForm()
    fetch_record = collection.find_one({"cust_id": 12345678})

    object_id = fetch_record['_id']


    if form.validate_on_submit():
        user = collection.find_one({"username": form.username.data})
        if user:
            if collection.find_one({'password': form.password.data}):
                flash(f'Welcome {user["name"]}', 'success')
                session['username'] = form.username.data
            else:
                flash('Please enter a correct password', 'danger')
        else:
            flash(f'No such username {form.username.data} exists', 'danger')
        # Add scholars form
    if ScholarsForm.validate_on_submit():
        scholar_name = ScholarsForm.name.data
        scholar_designation = ScholarsForm.designation.data
        scholar_bio = ScholarsForm.bio.data
        scholar_specialization = ScholarsForm.specialization.data
        picture_file = save_picture(ScholarsForm.photo.data, scholar_name)
        data = {"scholars":
            {
                "scholar_name": scholar_name,
                "scholar_designation": scholar_designation,
                "scholar_bio": scholar_bio,
                "scholar_specialization": scholar_specialization,
                "img": picture_file
            }}

        request = collection.update({"_id": object_id},
                                    {"$push": data},
                                    upsert=True
                                    )
        return redirect(url_for('addScholars'))

    # View all scholars.

    scholarsList = fetch_record['scholars']
    print(scholarsList)

    return render_template('scholars.html', form=form, scholarsForm=ScholarsForm, scholarsList=scholarsList, username=session['username'])


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['username'] = None
    return redirect('home')

"""
Add Projects 
"""
@app.route("/publications", methods=['GET', 'POST'])
def addPublications():
    if session.get('username') == None:
        session['username'] = None


    projectsForm = addProjects()
    fetch_record = collection.find_one({"cust_id": 12345678})

    object_id = fetch_record['_id']

    form = loginForm()
    if form.validate_on_submit():
        user = collection.find_one({"username": form.username.data})
        if user:
            if collection.find_one({'password': form.password.data}):
                flash(f'Welcome {user["name"]}', 'success')
                session['username'] = form.username.data
            else:
                flash('Please enter a correct password', 'danger')
        else:
            flash(f'No such username {form.username.data} exists', 'danger')
        # Add scholars form

    if projectsForm.validate_on_submit():
        title = projectsForm.title.data
        type = projectsForm.type.data
        location = projectsForm.location.data
        year = projectsForm.year.data
        link = projectsForm.link.data

        data = {"projects":
            {
                "project_title": title,
                "type": type,
                "location": location,
                "year": year,
                "link": link
            }}

        request = collection.update({"_id": object_id},
                                    {"$push": data},
                                    upsert=True
                                    )
        return redirect(url_for('addPublications'))

    # View all scholars.
    publicationsList = collection.find_one()['projects']
    return render_template('projects.html', form=form, projectsForm=projectsForm, publicationsList=publicationsList,
                               username=session['username'])



