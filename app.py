from flask import Flask, render_template, request,redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL')

if not database_url:
    raise RuntimeError("DATABASE_URL is not set or empty")
    
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.secret_key = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'signups'

    id = db.Column(db.Integer,primary_key=True) 
    name = db.Column(db.String(80),nullable=False)
    surname = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    phonenumber = db.Column(db.String(25),nullable=False)


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer,primary_key=True) 
    name = db.Column(db.String(80),nullable=False)
    surname = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    phonenumber = db.Column(db.String(25),nullable=False)
    message = db.Column(db.String(500),)


 
    
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signups', methods=['POST', 'GET'])
def signup():
    if request.method ==  'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        phonenumber = request.form['phone']

        new_user = User(name=name,surname=surname,email=email,phonenumber=phonenumber)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('success'))
    
    return render_template("index.html")



@app.route('/contacts', methods=['POST', 'GET'])
def contact():
    if request.method ==  'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        phonenumber = request.form['phone']
        message = request.form['message']

        new_message = Contact(name=name,surname=surname,email=email,phonenumber=phonenumber,message=message)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('success'))
    
    return render_template("index.html")



@app.route('/success')
def success():
    return render_template("success.html")



@app.route('/admin')
def admin():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    
    signups = User.query.all()
    contacts = Contact.query.all()

    return render_template("admin.html", signups=signups, contacts=contacts)


@app.route('/admin/login', methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "Admin1" and password == "Buddy2005":
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        return render_template("login.html", error="INVALID USER")
    return render_template("login.html")


@app.route('/admin/logout')
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


if __name__ == '__main__':
    app.run(debug=False,port=5500)                                                                                                                                                                                                                                                                                                                                                                                                               
