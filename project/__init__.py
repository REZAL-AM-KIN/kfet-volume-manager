import threading

import schedule
from flask import Flask
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
from .settings import LDAP_BASE_DN, REQUIRED_GROUPS, I2C_POTAR_ADRESS, DEV
from .slider_driver import setValue


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("settings.py")

    db.init_app(app)

    login_manager = LoginManager(app)
    ldap_manager = LDAP3LoginManager(app)
    login_manager.login_view = 'auth.login'

    from .task_runner import Task_runner
    task_runner = Task_runner(app)


    if not DEV:
        import board
        import adafruit_ds3502
        print("I2C init")
        i2c = board.I2C()
        # Initialisation de l'objet potentiomètre
        app.potentiometer = adafruit_ds3502.DS3502(i2c)
        print("I2C init pass")
    else:
        print("DEV MODE, NO I2C !!")

    from .models import User
    from .models import Slider

    # Declare a User Loader for Flask-Login.
    # Simply returns the User if it exists in our 'database', otherwise
    # returns None.
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    # Declare The User Saver for Flask-Ldap3-Login
    # This method is called whenever a LDAPLoginForm() successfully validates.
    # Here you have to save the user, and return it so it can be used in the
    # login controller.
    @ldap_manager.save_user
    def save_user(dn, username, data, memberships):
        user_id = int(data.get("uid")[0])
        #Extract group cn:
        memberships_cn = [group.get('cn')[0] for group in memberships]
        required_group = REQUIRED_GROUPS
        print(required_group)
        print(True if required_group else False)
        print(len(required_group))

        if (not required_group) or any(membership in required_group for membership in memberships_cn):
            user = User.query.filter_by(id=user_id).first()
            if not user:
                user = User(
                    id=int(user_id),
                    dn=dn,
                    username=username,
                    memberships=memberships_cn
                )
                db.session.add(user)
                db.session.commit()

            return user
        return "Unautorized"

    with app.app_context():
        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # Create Database Models
        print("Creating database")
        db.create_all()

        # Creation of slider
        if len(Slider.query.all()) == 0:
            print("No slider found id db : creation of slider")
            slider = Slider(
                value=0
            )
            db.session.add(slider)
            db.session.commit()

        if len(Slider.query.all()) != 1:
            print("Error, multiple slider : cleaning up database")
            # Delete all entries in the Slider table
            db.session.query(Slider).delete()
            # Commit the changes to the database
            db.session.commit()

        setValue(db.session.query(Slider).first())

        schedule.every().minute.at(":00").do(task_runner.schedule_changes)
        task_thread = threading.Thread(target=task_runner.run_scheduler)
        task_thread.start()

        return app
