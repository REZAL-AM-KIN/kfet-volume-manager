from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_ldap3_login.forms import LDAPLoginForm
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Instantiate a LDAPLoginForm which has a validator to check if the user
    # exists in LDAP.
    form = LDAPLoginForm()

    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object
        # via form.user.
        if form.user == "Unautorized":
            flash("Vous n'êtes pas autorisé à accéder à cette ressource")
            return render_template("login.html", form=form)
        if request.form.get('remember'):
            login_user(form.user, remember=True)
        else:
            login_user(form.user)
        return redirect("/")
    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for("auth.login"))
