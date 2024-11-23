from flask import Blueprint 

bp = Blueprint("survey" , __name__)

from . import routes
