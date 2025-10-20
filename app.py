from flask import Flask, render_template, request,redirect,session,url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "Jamal100%"

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS signups(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
                ) 
            ''')
    
    c.execute(''' CREATE TABLE IF NOT EXISTS contacts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                message TEXT NOT NULL 
                ) 
            ''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phone = request.form['phone']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO signups (name, surname, email, phone) VALUES (?, ?, ?, ?)', (name,surname,email,phone))
    conn.commit()
    conn.close()

    return redirect('success')


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO contacts (name, surname, email, phone, message) VALUES (?, ?, ?, ?, ?)', (name,surname,email,phone,message))
    conn.commit()
    conn.close()

    return redirect('success')

@app.route('/success')
def success():
    return render_template("success.html")



@app.route('/admin')
def admin():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM signups ORDER BY id DESC")
    signups = c.fetchall()

    c.execute("SELECT * FROM contacts ORDER BY id DESC")
    contacts = c.fetchall()

    conn.close()

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
    app.run(debug=True,port=5500)