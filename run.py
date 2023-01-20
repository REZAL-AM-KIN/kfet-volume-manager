#run.py
#Use for gunicorn launche in production
from dotenv import load_dotenv

from project import create_app

load_dotenv('.env')
app = create_app()

#Now you can run "gunicorn run:app" to launche the app in production
