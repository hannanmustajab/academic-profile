import os

from flask import render_template, url_for, redirect, flash, session

from application import app, bcrypt, Session
from application.forms import researchScholarsForm, loginForm
from application.connection import collection
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
    return render_template('home.html', scholarsList=scholarsList, form=form, username=session['username'])


@app.route("/addscholars", methods=['GET', 'POST'])
def addScholars():
    if session.get('username') == None:
        session['username'] = None

    ScholarsForm = researchScholarsForm()
    fetch_record = collection.find_one({"cust_id": 12345678})

    object_id = fetch_record['_id']

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

    return render_template('scholars.html', form=ScholarsForm, scholarsList=scholarsList, username=session['username'])


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['username'] = None
    return redirect('home')