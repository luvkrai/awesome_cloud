import docker
from flask import Flask, jsonify, request
import json

def initialize_docker():
	client = docker.DockerClient(base_url='tcp://10.249.112.106:2375', tls=False)
	return client

def getDocker():
	client = initialize_docker()
	result = []
	for container in client.containers.list():
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
@app.route("/launch_container",methods=['GET', 'POST'])
def launch_container():
	content = request.json
	client = initialize_docker()
	container = client.containers.run(content['image'], content['command'],detach=True)
	if container:
		return jsonify({'result': 'True'})
	else:
		return jsonify({'result': 'False'})
	
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=50001,debug=True)