#!/usr/bin/python3
"""dynamically generate web content"""
from flask import Flask, render_template, make_response, abort
from uuid import uuid4
from models import storage

app = Flask(__name__)

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
    app.run(port=5000, host="0.0.0.0", debug=True, threaded=True)
