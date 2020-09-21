from flask import Blueprint

main = Blueprint('main', __name__)

try:
    from . import views
except:
    pass
