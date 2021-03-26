from flask import Flask, render_template, request, g, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, \
    current_user, login_required, logout_user

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


@app.route("/")
@app.route("/entries")
def index():
    entry = models.Entry.select().limit(100).order_by(models.Entry.date.desc())
    return render_template("index.html", entry=entry)


@app.route("/entries/new", methods=("GET", "POST"))
def new_entry():
    pass


@app.route("/entries/<int:id>", methods=("GET", "POST"))
def get_entry():
    pass


@app.route("/entries/<int:id>/edit", methods=("GET", "POST"))
def edit_entry():
    pass


@app.route("/entries/<int:id>/delete", methods=("GET", "POST"))
def delete_entry():
    pass


if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT, host=HOST)
