from flask import render_template, request, redirect, url_for, abort

from flask_login import login_required, current_user
from ..models import Student, Courses, Exercise
from .forms import UpdateProfile

# importing main from main blueprint
from . import main
# importing database
from .. import db,photos

@main.route('/')
def index():

    '''
    View of root page function that returns the index page and its data
    '''
    
    return render_template('index.html')

@main.route('/html')
def html():
    '''
    View of page that has html course
    '''

    return render_template('my_html.html')

@main.route('/css')
def css():
    '''
    View of page that has css course
    '''
    return render_template('my_css.html')

@main.route('/science')
def science():
    '''
    View of page that has computer science course
    '''
    return render_template('science.html')

@main.route('/user/<username>')
def profile(username):

    '''
    View of page function that returns the the user's profile
    '''

    user = Student.query.filter_by(username = username).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<username>/update',methods = ['GET','POST'])
@login_required
def update_profile(username):
    user = Student.query.filter_by(username = username).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',username=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<username>/update/pic',methods= ['POST'])
@login_required
def update_pic(username):
    user = Student.query.filter_by(username = username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',username=username))
