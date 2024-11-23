from flask import Blueprint 

bp = Blueprint("wallet" , __name__)

from . import routes
