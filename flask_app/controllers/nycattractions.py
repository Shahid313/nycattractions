from flask import Flask, render_template, session, redirect,flash, request, url_for
from flask_app import app
from flask_app.utils import save_file
from flask_app.config.config import conn
from flask_app.controllers.user import *

@app.route('/new', methods=['GET', 'POST'])
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        return render_template('post.html')

@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        if request.method == 'POST':
            post_description = request.form.get('post_description')
            post_picture = request.files['post_picture']
            print(post_picture)
            isSaved, file_name = save_file(post_picture,'user_images')
            print(file_name)
            conn.execute("INSERT INTO nyc_attractions (post_picture,post_description,user_name, user_id) VALUES (%s, %s, %s, %s) ", (file_name,post_description,session['user_name'], session['user_id']))
            return redirect('/dashboard')

@app.route('/like/<int:id>/<int:user_id>')
def like(id, user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        existed_like = conn.execute("SELECT * FROM post_like WHERE like_by_id = %s AND liked_post_id = %s",(session['user_id'],id))
        print(existed_like)
        if existed_like:
            conn.execute("DELETE FROM post_like WHERE like_by_id = %s AND liked_post_id = %s", (session['user_id'],id))
            return redirect('/dashboard')
        else:
            conn.execute("INSERT INTO post_like (like_by_id,liked_post_id, person_whose_post_is_liked) VALUES (%s, %s, %s) ", (session['user_id'],id,user_id))
            return redirect('/dashboard')

@app.route('/delete_post/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        conn.execute("DELETE FROM nyc_attractions WHERE id = %s", (id))
        return redirect('/dashboard')


@app.route('/update_post/<int:id>', methods=['GET', 'POST'])
def update_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        if request.method == 'POST':
            up_description = request.form.get('post_description')
            up_picture = request.files['post_picture']
            isSaved, file_name = save_file(up_picture,'user_images')
            conn.execute("UPDATE nyc_attractions SET post_picture = %s, post_description = %s WHERE id = %s", (file_name,up_description,id))
            return redirect('/dashboard')
        else:
            return render_template('update_post.html', id=id)

@app.route('/profile_details/<int:id>')
def profile_details(id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        conn.execute("Select *,(select count(*) from post_like where person_whose_post_is_liked=user.id) as total_likes_count, (select count(*) from nyc_attractions where nyc_attractions.user_id=user.id) as total_posts_counts from user WHERE user.id="+str(id))
        user_details = conn.fetchall()
        print(user_details)
        return render_template('profile_details.html', user_details=user_details)


@app.route('/post_details/<int:id>')
def post_details(id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        conn.execute("SELECT * FROM nyc_attractions  LEFT JOIN user on user.id=nyc_attractions.user_id WHERE nyc_attractions.id="+str(id))
        post_details = conn.fetchall()
       

        conn.execute("SELECT * FROM post_like LEFT JOIN user on user.id=post_like.like_by_id WHERE post_like.liked_post_id="+str(id))
        post_liked_users_details = conn.fetchall()
        
        return render_template('post_details.html', post_details=post_details,post_liked_users_details=post_liked_users_details)

