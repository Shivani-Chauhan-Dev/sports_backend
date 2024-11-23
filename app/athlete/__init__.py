from flask import Blueprint 

bp = Blueprint("athlete" , __name__)

from . import routes