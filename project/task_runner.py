from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class Task_runner:
    def __init__(self, app):
        self.app = app
        self.scheduler = BackgroundScheduler()

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
            # clear all the scheduled tasks
            self.scheduler.remove_all_jobs()

            # Get all the changes
            automations = db.session.query(Automation).all()
            # Schedule the change_slider_value function to run at the specified hour
            for automation in automations:
                hour, minute = automation.time.split(":")
                self.scheduler.add_job(self.change_slider_value, trigger=CronTrigger(hour=hour, minute=minute),
                                       args=[automation.id])
                print("Add routine: value " + str(automation.value) + " at " + automation.time)
        print("reloading completed")

    def run_scheduler(self):
        print("Task scheduler started")
        self.scheduler.start()

        # Schedule the task_runner.schedule_changes to run every minute
        self.scheduler.add_job(self.schedule_changes, 'interval', minutes=1)
