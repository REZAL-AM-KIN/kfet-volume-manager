from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user

from . import db, slider_driver
from .models import Slider, Automation
from .settings import MAX_DISPLAY_GROUPS

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    slider = db.session.query(Slider).first()
    automations = db.session.query(Automation).all()
    if (not MAX_DISPLAY_GROUPS) or any(membership in MAX_DISPLAY_GROUPS for membership in current_user.memberships):
        displayMax = True
    else:
        displayMax = False
    return render_template('slider.html', user=current_user, slider=slider, displayMax=displayMax, automations=automations)


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


@login_required
@main.route('/add_automation', methods=['POST'])
def add_automation():

    time = request.form['time_automation']
    value = request.form['slider_value_automation']

    if not time:
        flash("Vous devez entrer une heure")
        return redirect("/")

    if not value:
        flash("Vous devez entrer une valeur")
        return redirect("/")

    automation = Automation(time=time, value=value)
    db.session.add(automation)
    db.session.commit()

    return redirect("/")


@login_required
@main.route("/delete_automation", methods=['GET'])
def delete_automation():
    automation_id = request.args.get('id')
    if not automation_id:
        flash("no id received, please contact rezal.")
        return redirect("/")
    automation = db.session.query(Automation).get(automation_id)
    db.session.delete(automation)
    db.session.commit()
    return redirect('/')


