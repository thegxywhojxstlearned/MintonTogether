import code
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db
from datetime import datetime
import haversine as hs
import geocoder

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@views.route("/home")
@login_required
def home():
    if request.method == "POST":
        filter_discipline = request.form.get('filter_discipline')
        posts = Post.query.filter_by(badminton_discipline=filter_discipline)

        return render_template("home.html", user=current_user, posts=posts)

    else:

        posts = Post.query.all()
        return render_template("home.html", user=current_user, posts=posts)

    # if request.method == "POST":
    #     filter_discipline = request.form.get('filter_discipline')
    #     location = request.form.get('location')
    #     my_location= geocoder.ip('me')

    #     #my latitude and longitude coordinates
    #     latitude= my_location.geojson['features'][0]['properties']['lat']
    #     longitude = my_location.geojson['features'][0]['properties']['lng']

    #     for loc in Post.query.filter_by(location=location):

        


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        discipline = request.form.get('badminton_discipline')
        eventtime = request.form.get("eventtime")
        date = request.form.get("eventdate")
        date_format = datetime.strptime(date, '%Y-%m-%d')
        eventdate = date_format.strftime('%d/%m/%Y')
        location = request.form.get('location')
        
        
        if not discipline and not eventtime:
            if not location:
                flash('Post cannot be empty', category="error")
        else:
            post = Post(badminton_discipline=discipline, eventtime=eventtime, eventdate=eventdate, location=location,author=current_user.id) # add the modles <
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
            
        # if not discipline:
        #     flash('Post cannot be empty', category='error')
        # else:
        #     post = Post(badminton_discipline=discipline,author=current_user.id) # add the modles <
        #     db.session.add(post)
        #     db.session.commit()
        #     flash('Post created!', category='success')
        #     return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)
