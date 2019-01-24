from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, login_required
from flaskblog.models import User
import requests

main = Blueprint('main', __name__)


@main.route("/home")
@login_required
def home():
    r = requests.get('http://10.249.112.106:5000/docker')
    return render_template('home.html', user=current_user,text=r.text)


@main.route("/about")
@login_required
def about():
    return render_template('about.html', title='About')
