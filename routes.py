from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app,db,bcrypt
from flask_login import login_user
posts = [
    {
        'author':'dharm r',
        'title':'Assignment 1',
        'content':'first post',
        'date_posted':'oct 12,2020',
        'date_submit':'oct 25,2020'
    },
    {
        'author':'jay r',
        'title':'Assignment 2',
        'content':'second post',
        'date_posted':'oct 13,2020',
        'date_submit':'oct 26,2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)
@app.route("/about")
def about():
    return render_template("about.html", title ='about')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_passsword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data,password=hashed_passsword)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! you can login now', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title = 'Register',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('login unsuccessful.please check email or password','danger')

    return render_template('login.html',title = 'login',form=form)
