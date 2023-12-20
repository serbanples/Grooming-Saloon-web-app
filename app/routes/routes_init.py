#repo/app/routes/__init__.py
from flask import Blueprint

main = Blueprint('main', __name__)

from app.routes.routes_init import main  # Import main module
