from enum import unique
from flask import Flask, render_template, request, g, url_for, session, redirect, before_render_template
from flask_cors import CORS
from send_email import send_email
from flask_sqlalchemy import SQLAlchemy
import os 
import functools
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort


dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
bdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.secret_key = "1234567"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    dimentions = db.Column(db.String(20))
    primary_photo = db.Column(db.String(60))
    secondary_photo_one = db.Column(db.String(60))
    secondary_photo_two = db.Column(db.String(60))
    secondary_photo_three = db.Column(db.String(60))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(99))
    

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.before_request
def load_logged_in_admin():
    admin_id = session.get('admin_id')
    if admin_id is None:
        g.admin = None
    else:
        g.admin = admin_id

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('admin_login'))
        
        return view(**kwargs)

    return wrapped_view

@app.route('/')
def main():
    items = Item.query.all()

    return render_template('main.html', items = items)

@app.route('/item/<id>')
def get_full_item(id):
    item = Item.query.filter_by(id=id).first()
    
    return render_template('item.html', item = item)

@app.route('/message', methods=['POST'])
def post_message():
    if request.method == 'POST':
        form = request.json
        name = form['name']
        email = form['email']
        number = form['number']
        message = form['message']
        send_email(name, email, number, message)
        return 'received'


@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':

        form_email = request.form['email']
        form_password = request.form['password']

        admin = Admin.query.filter_by(email=form_email).first()

        if admin:
             if check_password_hash(admin.password, form_password):
                session.clear()
                session['admin_id'] = admin.id
                return redirect(url_for('main_admin'))

    return render_template('admin_login.html')

@app.route('/admin')
@login_required
def main_admin():
    items = Item.query.all()
    return render_template('admin.html', items = items)


def form_request():
    form_name = request.form['name']
    form_dimentions = request.form['dimentions']
    form_description = request.form['description']
    form_primary_photo = request.form['first_photo']
    form_secondary_photo_one = request.form['second_photo']
    form_secondary_photo_two = request.form['third_photo']
    form_secondary_photo_three = request.form['fourth_photo']
    form_item = Item(name=form_name, description=form_description ,dimentions=form_dimentions, primary_photo=form_primary_photo, secondary_photo_one=form_secondary_photo_one, secondary_photo_two=form_secondary_photo_two, secondary_photo_three=form_secondary_photo_three)

    return form_item

@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        item = form_request()
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('main_admin'))

    return render_template('admin_add.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    if request.method == 'POST':
        item = form_request()
        
        query_item = Item.query.filter_by(id=id).first()
        query_item.description = item.description
        db.session.commit()


        return redirect(url_for('main_admin'))

    query_item = Item.query.filter_by(id=id).first()
    return render_template('admin_edit.html', item = query_item)

@app.route('/delete/<id>')
def delete_item(id):
    query_item = Item.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main_admin'))

@app.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    db.create_all()
    app.run(port=5000, debug=True)
