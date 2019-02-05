from flask import render_template, request, Blueprint, flash
from flask_login import login_user, current_user, login_required
from flaskblog.docker_data.forms import LaunchContainer
import requests
from flask_cors import cross_origin
import json

docker = Blueprint('docker', __name__)


@docker.route("/launch_container", methods=['GET','POST'])
@login_required
def launch_container():
    form = LaunchContainer()
    if form.validate_on_submit():
        r = requests.post('http://localhost:50001/launch_container',json={'image':form.image.data,'command':form.command.data})
        if r.ok:
            flash('A container has been created!', 'success')
        else:
            flash('Error!! Could not create the container', 'danger')
    return render_template('launch.html', title='Launch Container',
                           form=form, legend='New Container')

@docker.route("/exited_container")
@login_required
#@cross_origin(supports_credentials=True)
def exited_container():
	r = requests.get('http://localhost:50001/exited_container')
	table = r.json()
	return render_template('exited.html',user=current_user,table=table)

@docker.route("/delete_container/<data>",methods=['GET', 'POST'])
def delete_container(data):
    r = requests.get('http://localhost:50001/delete_container/'+data)
    res = r.json()
    r1 = requests.get('http://localhost:50001/exited_container')
    if r.ok and r1.ok:
        pass
    table = r1.json()
    return json.dumps({'table':table, 'success':res['success']})
    #return str(r.json())