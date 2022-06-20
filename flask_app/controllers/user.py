from flask import Flask, render_template, session, redirect,flash, request, url_for
from flask_app import app
from flask_app.config.config import conn, connection
from flask_bcrypt import Bcrypt
from flask_app.controllers.nycattractions import *
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password != confirm:
            flash("The passwords does not match")
            return redirect('/')
        else:
            hashed_password = bcrypt.generate_password_hash(password)
            conn.execute("INSERT INTO user (first_name,last_name,email,password) VALUES (%s, %s, %s, %s) ", (first_name,last_name,email,hashed_password))
            flash("Registered succesfully please login")
            return redirect('/')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = conn.execute("SELECT * FROM user WHERE email = %s",(email))
        required_user = conn.fetchall()
        if user:
            if bcrypt.check_password_hash(required_user[0]['password'], password):
                session['user_id'] = required_user[0]['id']
                session['user_name'] = required_user[0]['first_name']+" "+required_user[0]['last_name']
                return redirect('/dashboard')
            else:
                flash("The password is incorrect")
                return redirect('/')
        else:
            flash("The email does not exist")
            return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        conn.execute("SELECT *,(select count(*) from post_like where post_like.liked_post_id=nyc_attractions.id) as likes_count FROM nyc_attractions LEFT JOIN user on user.id=nyc_attractions.user_id  ")
        posts = conn.fetchall()
        print(posts)
        return render_template('dashboard.html', posts=posts)



