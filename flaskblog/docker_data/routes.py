from flask import render_template, request, Blueprint, flash
from flask_login import login_user, current_user, login_required
from flaskblog.docker_data.forms import LaunchContainer
import requests

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
            flash('Could not create the container', 'danger')
    return render_template('launch.html', title='Launch Container',
                           form=form, legend='New Container')

