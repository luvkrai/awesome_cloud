from flask import render_template, request, Blueprint, flash
from flask_login import login_user, current_user, login_required
from flaskblog.docker_data.forms import LaunchContainer
from flaskblog.models import User, Containers
from flaskblog import db
import requests
import json

docker = Blueprint('docker', __name__)


def filter_containers_by_user(table):
    user = User.query.filter_by(username=current_user.username).first()
    containers = Containers.query.filter_by(creator=user).all()
    new_table = []
    for row in table:
        conObj,result = find_container(row['container_id'],containers)
        if result:
            row['date'] = conObj.data_created.strftime('%Y-%m-%d')
            new_table.append(row)
    return new_table

def find_container(cid,containers):
    for container in containers:
        if cid == container.container_id:
            return container, True
    return None, False

@docker.route("/launch_container", methods=['GET','POST'])
@login_required
def launch_container():
    form = LaunchContainer()
    if form.validate_on_submit():
        name = ""
        if form.name.data:
            name = form.name.data
        r = requests.post('http://localhost:50001/launch_container',json={'image':form.image.data,'command':form.command.data,'name':name})
        res = r.json()
        if r.ok:
            container = Containers(container_id=res['container_id'], image=form.image.data, creator=current_user)
            db.session.add(container)
            db.session.commit()
            flash('A container has been created!', 'success')
        else:
            flash('Error!! Could not create the container', 'danger')
    return render_template('launch.html', title='Launch Container', user=current_user,
                           form=form, legend='New Container')

@docker.route("/exited_container")
@login_required
def exited_container():
    r = requests.get('http://localhost:50001/exited_container')
    table = r.json()
    table = filter_containers_by_user(table)
    return render_template('exited.html',user=current_user,table=table)

@docker.route("/delete_container/<data>",methods=['GET', 'POST'])
def delete_container(data):
    r = requests.get('http://localhost:50001/delete_container/'+data)
    res = r.json()
    if r.ok:
        for container_id in data.split(','):
            container = Containers.query.filter_by(container_id=container_id).first()
            db.session.delete(container)
        db.session.commit()
    r1 = requests.get('http://localhost:50001/exited_container')
    table = r1.json()
    table = filter_containers_by_user(table)
    print(table)
    return json.dumps({'table':table, 'success':res['success']})
