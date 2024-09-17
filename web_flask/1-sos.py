#!/usr/bin/python3
"""dynamically generate web content"""
from flask import Flask, render_template, make_response, abort
from uuid import uuid4
from models import storage
from os import getenv

app = Flask(__name__) #static_folder='static'

@app.teardown_appcontext
def close(error):
    storage.close()
@app.route("/", strict_slashes=False)
@app.route("/softsphere", strict_slashes=False)
def home():
    """ SoftSphere is Alive! """
    categories = storage.all("Category").values()
    categories = sorted(categories, key=lambda k: k.name)
    projects = storage.all("Project").values()
    projects = sorted(projects, key=lambda k: k.name)
    tools = storage.all("Tool").values()
    tools = sorted(tools, key=lambda k: k.name)
    # users = storage.all("User").values()
    return render_template("1-index.html",
                           categories=categories,
                           projects=projects,
                           tools=tools,
                           cache_id=uuid4())

@app.route("/projects/<project_name>", strict_slashes=False)
def show_project(project_name):
    """return project representation page"""
    result = storage.filter("Project", "name", "eq", project_name)
    if not result:
        abort(404)
    project = result[0]
    category_projects = storage.filter("Project", "category_id", "eq", project.category_id)
    category_projects = sorted(category_projects, key=lambda k: (k.rate, k.name))
    category_projects.remove(project)
    return render_template("project.html",
                           project=project,
                           category_projects=category_projects,
                           cache_id=uuid4())

@app.route("/users/<username>/projects", strict_slashes=False)
def show_user_projects(username):
    """return user project page"""
    result = storage.filter("User", "username", "eq", username)
    if not result:
        abort(404)
    user = result[0]
    return render_template("user.html",
                            user=user,
                            cache_id=uuid4())


    
if __name__ == "__main__":
    host = getenv("SOS_HOST", "0.0.0.0")
    port = int(getenv("SOS_PORT", 5000))
    app.run(port=port, host="0.0.0.0", debug=True, threaded=True)

"""
[Unit]
Description=Gunicorn instance to serve SoftSphere
After=network.target

[Service]
User=ubuntu
group=www-data
WorkingDirectory=/home/ubuntu/SoftSphere_v3
ExecStart=/usr/bin/gunicorn --workers 3 --bind 0.0.0.0:5005 --env SOS_STORAGE_TYPE="db" web_flask.1-sos:app
StandardError=/tmp/sos-error.log
StandardOutput=/tmp/sos-access.log
Restart=always

[Install]
WantedBy=multi-user.target
"""

"""
[Unit]
Description=Gunicorn instance to serve SoftSphere apis
After=network.target

[Service]
User=ubuntu
group=www-data
WorkingDirectory=/home/ubuntu/SoftSphere_v3
ExecStart=/usr/bin/gunicorn --workers 3 --bind 0.0.0.0:5004 --env SOS_STORAGE_TYPE="db" api.v1.app:app
StandardError=/tmp/sos_api-error.log
StandardOutput=/tmp/sou_api-access.log
Restart=always

[Install]
WantedBy=multi-user.target
"""

"""
server {
    listen 80;
    server_name softsphere.maherai.tech;
    add_header X-Serverd-By: "433823-web-02";
    error_page 404 /404.html;

    location /softsphere {
        proxy_pass http://localhost:5005;
    }

    location ~ ^/softsphere/projects/.+$ {
        rewrite ^/softsphere/(projects/.+)$ /$1 break;
        proxy_pass http://localhost:5005;
    }

    location ~ ^/softsphere/users/.+/projects$ {
        rewrite ^/softsphere/(users/.+/projects)$ /$1 break;
        proxy_pass http://localhost:5005;
    }

    location ~ ^/softsphere/api/v1/.* {
        rewrite ^/softsphere/(api/v1/.*)$ /$1 break;
        add_header 'Access-Control-Allow-Origin' '*';
        proxy_pass http://localhost:5004;
    }
}
"""