import schedule
import time
from datetime import datetime
from project.models import Automation, Slider
from project import db, setValue


#Ce script doit être exécuter à part, il est en charge d'effectuer les changement sur la base de donnée
from wsgi import app


def change_slider_value(automation_id):
    # Get the automation for the current hour
    automation = db.session.query(Automation).get(automation_id)

    # Get the first slider
    slider = db.session.query(Slider).first()
    slider.value = automation.value
    db.session.commit()
    setValue(slider)


@schedule.repeat(schedule.every().minutes)
def schedule_changes():
    with app.app_context():
        print("reloading automation tasks")
        schedule.clear()
        # Get all the changes
        automations = db.session.query(Automation).all()
        # Schedule the change_slider_value function to run at the specified hour
        for automation in automations:
            schedule.every().day.at(f"{automation.time.strftime('%H:%M')}").do(change_slider_value, automation_id=automation.id)


while True:
    schedule.run_pending()
    time.sleep(1)
