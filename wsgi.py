#wsgi.py
#Use for gunicorn launche in production
import threading

from dotenv import load_dotenv

from project import create_app
from project.task_runner import run_scheduler

load_dotenv('.env')
app = create_app()


task_thread = threading.Thread(target=run_scheduler)
task_thread.start()

#Now you can run "gunicorn wsqi:app" to launche the app in production
