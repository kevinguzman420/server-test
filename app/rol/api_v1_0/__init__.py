from flask import Blueprint

rol_bp = Blueprint('rol', __name__)

from . import resources
