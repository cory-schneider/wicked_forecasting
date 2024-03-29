from flask import render_template, redirect, request, Blueprint, flash, url_for
from forecastapp.models import Post, User
from forecastapp import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from forecastapp.users.forms import LoginForm

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    login_form = LoginForm()
    if current_user.is_authenticated:
        title = current_user.username
    else:
        title = "Log In"
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('home.html', login_form=login_form,
                                    legend='Wicked Weed Inventory Management',
                                    title=title)


@main.route("/messages")
def messages():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('messages.html', posts=posts, title='Messaging')


@main.route("/about")
def about():
    return render_template('about.html', title='About', legend="About")
