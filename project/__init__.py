from flask import Flask
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("settings.py")

    db.init_app(app)

    login_manager = LoginManager(app)
    ldap_manager = LDAP3LoginManager(app)
    login_manager.login_view = 'auth.login'



    from .models import User

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
        print(username)
        user_id = int(data.get("uid")[0])

        user = User.query.filter_by(id=user_id).first()
        if not user:
            user = User(
                id=int(user_id),
                dn=dn,
                username=username
            )
            db.session.add(user)
            db.session.commit()

        return user

    with app.app_context():
        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # Create Database Models
        print("creating database")
        db.create_all()


        return app
