from flask import Blueprint, render_template
from flask_login import login_required, current_user

from . import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return "Hello "+current_user.username + "<br/> Vous groupes sont: " + ", ".join(current_user.memberships)
