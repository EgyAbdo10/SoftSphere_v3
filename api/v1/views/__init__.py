#!/usr/bin/env python3
"""
will comment when everything works as needed

"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.projects_view import *
from api.v1.views.categories_view import *
from api.v1.views.tools_view import *
from api.v1.views.users_view import *