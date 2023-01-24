import schedule
import time

from flask import current_app


class Task_runner:
    def __init__(self, app):
        self.app = app

    def change_slider_value(self, automation_id):
        from . import db, setValue
        from .models import Automation, Slider
        print("enter in job")
        try:
            with self.app.app_context():
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


    def schedule_changes(self):
        from . import db
        from .models import Automation
        print("reloading automation tasks")
        with self.app.app_context():
            schedule.clear()
            # Get all the changes
            automations = db.session.query(Automation).all()
            # Schedule the change_slider_value function to run at the specified hour
            for automation in automations:
                schedule.every().day.at(f"{automation.time}").do(self.change_slider_value, automation_id=automation.id)
                print("Add routine: value "+str(automation.value)+" at "+automation.time)
        print("reloading completed")

    def run_scheduler(self):
        print("Task scheduler started")
        while True:
            schedule.run_pending()
            time.sleep(0.5)
