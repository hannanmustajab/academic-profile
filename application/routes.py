import os

from flask import render_template, url_for, redirect

from application import app
from application.forms import researchScholarsForm
from connection import collection
from scholars import scholarsList


def save_picture(form_picture, name):
    random_hex = name
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fname = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/users', picture_fname)
    form_picture.save(picture_path)

    return picture_fname


@app.route("/home")
def home():
    return render_template('home.html', scholarsList=scholarsList)


@app.route("/addscholars", methods=['GET', 'POST'])
def addScholars():
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

    return render_template('scholars.html', form=ScholarsForm, scholarsList=scholarsList)
