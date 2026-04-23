from flask import render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import re
from app import app
from db import get_db_connection


@app.route('/')
def home():
    return render_template("index.html")


from werkzeug.security import generate_password_hash, check_password_hash
import re

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        # Email validation
        pattern = r'^[A-Za-z0-9._%+-]+@campus\.com$'
        if not re.match(pattern, email):
            flash("Enter valid email", "danger")
            return redirect('/register')

        # Strong password check
        if len(password) < 8:
            flash("Password must be at least 8 characters", "danger")
            return redirect('/register')

        if not any(char.isupper() for char in password):
            flash("Password needs one uppercase letter", "danger")
            return redirect('/register')

        if not any(char.isdigit() for char in password):
            flash("Password needs one number", "danger")
            return redirect('/register')

        # Hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(name,email,password,role) VALUES(%s,%s,%s,%s)",
                (name, email, hashed_password, "user")
            )

            conn.commit()

            flash("Registration successful. Please login.", "success")
            return redirect('/login')

        except Exception:
            flash("Email already exists", "danger")
            return redirect('/register')

        finally:
            cur.close()
            conn.close()

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and check_password_hash(user['password'], password):

            session['user_id'] = user['user_id']
            session['name'] = user['name']
            session['role'] = user['role']

            flash("Login successful", "success")

            if user['role'] == 'admin':
                return redirect('/admin')

            return redirect('/dashboard')

        flash("Invalid email or password", "danger")
        return redirect('/login')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template("dashboard.html", name=session['name'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')