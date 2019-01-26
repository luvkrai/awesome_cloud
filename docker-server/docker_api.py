import docker
from flask import Flask, jsonify
import json

def getDocker():
    client = docker.DockerClient(base_url='tcp://10.249.112.106:2375', tls=False                                                                             )
    container = client.containers.run('alpine', 'sleep 1000',detach=True)
    container.logs()
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
def hello():
    return jsonify(getDocker())
    #return json.dumps(getDocker())
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=50001,debug=True)