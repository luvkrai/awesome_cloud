from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, login_required
from flaskblog.models import User, Containers
import requests

main = Blueprint('main', __name__)

def find_container(cid,containers):
	for container in containers:
		if cid == container.container_id:
			return container, True
	return None, False


@main.route("/home")
@login_required
def home():
	r = requests.get('http://localhost:50001/docker')
	table = r.json()
	user = User.query.filter_by(username=current_user.username).first()
	containers = Containers.query.filter_by(creator=user).all()
	new_table = []
	for row in table:
		conObj,result = find_container(row['container_id'],containers)
		if result:
			row['date'] = conObj.data_created.strftime('%Y-%m-%d')
			new_table.append(row)
	return render_template('home.html',user=current_user,table=new_table)


@main.route("/about")
@login_required
def about():
	return render_template('about.html', user=current_user, title='About')
