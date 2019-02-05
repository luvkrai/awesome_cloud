import docker
from flask import Flask, jsonify, request
import json

def initialize_docker():
	client = docker.DockerClient(base_url='tcp://10.249.112.106:2375', tls=False)
	return client

def getDocker(status=None):
	client = initialize_docker()
	result = []
	if status:
		container_list = client.containers.list(filters=status)
	else:
		container_list = client.containers.list()
	for container in container_list:
		if status:
			row = {
			'name': container.name,
			'container_id': container.short_id,
			'image': container.image.tags[0],
			'status': container.status,
			}
		else:
			row = {
				'name': container.name,
				'container_id': container.short_id,
				'image': container.image.tags[0],
				'status': container.status
			}
		result.append(row)
	return result

app = Flask(__name__)

@app.route("/docker")
def docker_container():
	dummy=[
  {
    "container_id": "71686da8da", 
    "image": "alpine:3.8", 
    "name": "focused_buck", 
    "status": "running"
  }, 
  {
    "container_id": "7594a76ee0", 
    "image": "alpine:3.8", 
    "name": "affectionate_margulis", 
    "status": "running"
  }
]
    #return jsonify(getDocker())
	#return jsonify(dummy)
	return json.dumps(getDocker())

@app.route("/exited_container")
def exited_container():
	dummy=[
  {
    "container_id": "71686da8da",
    "image": "alpine:3.8",
    "name": "focused_buck",
    "status": "running"
  },
  {
    "container_id": "7594a76ee0",
    "image": "alpine:3.8",
    "name": "affectionate_margulis",
    "status": "running"
  }
]
    #return jsonify(getDocker())
	#return jsonify(dummy)
	return json.dumps(getDocker({'status':'exited'}))


@app.route("/launch_container",methods=['GET', 'POST'])
def launch_container():
	content = request.json
	client = initialize_docker()
	container = client.containers.run(content['image'], content['command'],detach=True)
	if container:
		return jsonify({'result': 'True'})
	else:
		return jsonify({'result': 'False'})

@app.route("/delete_container/<data>",methods=['GET', 'POST'])
def delete_container(data):
	client = initialize_docker()
	try:
		exited_containers = client.containers.list(filters={'status':'exited'})
		for container in exited_containers:
			if container.short_id in data.split(','):
				container.remove()
		return jsonify({'success': True})
	except:
		return jsonify({'success': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=50001,debug=True)