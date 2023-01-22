from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from . import db, slider_driver
from .models import Slider
from .settings import MAX_DISPLAY_GROUPS

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    slider = db.session.query(Slider).first()
    if (not MAX_DISPLAY_GROUPS) or any(membership in MAX_DISPLAY_GROUPS for membership in current_user.memberships):
        displayMax = True
    else:
        displayMax = False
    return render_template('slider.html', user=current_user, slider=slider, displayMax=displayMax)


@login_required
@main.route('/slider_value', methods=['POST'])
def slider_value():
    value = request.get_json()["value"]
    slider = db.session.query(Slider).first()
    slider.value = value
    db.session.commit()
    slider_driver.setValue(slider)
    return "Value received"


@login_required
@main.route('/slider_max', methods=['POST'])
def slider_max():
    value = request.get_json()["max"]
    slider = db.session.query(Slider).first()
    slider.max = value
    db.session.commit()
    slider_driver.setValue(slider)
    return "Max received"

