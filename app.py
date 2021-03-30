from flask import Flask, render_template, g, url_for, abort, flash, redirect
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user,
                         current_user, login_required, logout_user)

import models
import forms

app = Flask(__name__)
app.secret_key = "707n#c983n,e!c^l?w*d(n9.84f2e_v707 "

DEBUG = True
PORT = 8080
HOST = "127.0.0.1"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "Login"


@app.before_request
def before_request():
    g.db = models.db
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.route("/login", methods=("GET", "POST"))
def login():
    form = forms.Login()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Email and Password DO NOT Match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've Been Logged In!", "success")
            else:
                flash("Email and Password DO NOT Match!", "error")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've Been Logged Out!", "success")
    return redirect(url_for("index"))


@app.route("/signup", methods=("GET", "POST"))
def sign_up():
    form = forms.SignUp()
    if form.validate_on_submit():
        flash("Congrats, You're Signed Up", "success")
        models.User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        return redirect(url_for("index"))
    return render_template("signup.html", form=form)


@app.route("/")
@app.route("/entries")
def index():
    entries = models.Entry.select().limit(100).order_by(models.Entry.date.desc())
    return render_template("layout.html", entries=entries)


@app.route("/entries/new", methods=("GET", "POST"))
def new_entry():
    form = forms.Entry()
    if form.validate_on_submit():
        models.Entry.create(
            user=g.user.get_current_object,
            title=form.title.data,
            date=form.date.data,
            est_time=form.est_time.data,
            i_learned=form.i_learned.data,
            resources=form.resources.data
        )
        flash("Entry Published and Saved", "success")
        return redirect(url_for("index"))
    return render_template("new.html", form=form)


@app.route("/entries/<int:id>", methods=("GET", "POST"))
def get_entry():
    entry = models.Entry.get(models.Entry.id == id)
    if entry.count() == 0:
        abort(404)
    return render_template("detail.html")


@app.route("/entries/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit_entry():
    try:
        entry = models.Entry.get(models.Entry.id == id)
        if current_user == entry.user:
            models.Entry.update(
                user=g.user.get_current_object,
                title=entry.title.data,
                date=entry.date.data,
                est_time=entry.est_time.data,
                i_learned=entry.i_learned.data,
                resources=entry.resources.data
            ).save()
            flash("Entry Has Been Updated!", "success")
    except models.DoesNotExist:
        abort(404)


@app.route("/entries/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete_entry():
    try:
        entry = models.Entry.get(models.Entry.id == id)
        if current_user == entry.user:
            entry.delete_instance()
            flash("Entry Deleted", "success")
    except models.DoesNotExist:
        abort(404)
    return redirect(url_for("index"))


@app.errorhandler(404)
def abort(error):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT, host=HOST)
