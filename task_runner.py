import schedule
import time
from datetime import datetime
from project.models import Automation, Slider
from project import db, setValue

from wsgi import app


def change_slider_value(automation_id):
    print("enter in job")
    try:
        with app.app_context():
            # Get the automation for the current hour
            automation = db.session.query(Automation).get(automation_id)
            # Get the first slider
            slider = db.session.query(Slider).first()
            slider.value = automation.value
            db.session.commit()
            setValue(slider)
            print("Value set to " + str(slider.value))
    except:
        import traceback
        print(traceback.format_exc())

@schedule.repeat(schedule.every().minutes)
def schedule_changes():
    print("reloading automation tasks")
    with app.app_context():
        schedule.clear()
        # Get all the changes
        automations = db.session.query(Automation).all()
        # Schedule the change_slider_value function to run at the specified hour
        for automation in automations:
            schedule.every().day.at(f"{automation.time}").do(change_slider_value, automation_id=automation.id)
            print("Add routine: value "+str(automation.value)+" at "+automation.time)
    print("reloading completed")


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
