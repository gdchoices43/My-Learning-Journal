from flask import Flask, render_template, g, url_for, abort, flash, redirect, request


import models
import forms

app = Flask(__name__)
app.secret_key = "707n#c983n,e!c^l?w*d(n9.84f2e_v707 "


@app.before_request
def before_request():
    g.db = models.db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route("/")
@app.route("/entries", methods=("GET", "POST"))
def index():
    stream = models.Entry.select().order_by(models.Entry.date.desc())
    return render_template("index.html", stream=stream)


@app.route("/entries/new", methods=("GET", "POST"))
def new_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data,
            date=form.date.data,
            time=form.time.data,
            i_learned=form.i_learned.data,
            resources=form.resources.data
        )
        flash("Saved and Published Entry", "success")
        return redirect(url_for("index"))
    return render_template("new.html", entry=form)


@app.route("/entries/<int:entry_id>")
def get_entry(entry_id):
    entries = models.Entry.select().where(models.Entry.id == entry_id)
    return render_template("detail.html", stream=entries)


@app.route("/entries/<int:entry_id>/edit", methods=("GET", "POST"))
def edit_entry(entry_id):
    entry = models.Entry.get(models.Entry.id == entry_id)
    form = forms.EntryForm()
    if request.method == "GET":
        form.title.data = entry.title
        form.date.data = entry.date
        form.time.data = entry.time
        form.i_learned.data = entry.i_learned
        form.resources.data = entry.resources
    elif form.validate_on_submit():
        entry.title = form.title.data
        entry.date = form.date.data
        entry.time = form.time.data
        entry.i_learned = form.i_learned.data
        entry.resources = form.resources.data
        flash("Saved Entry", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", form=form, entry=entry)


@app.route("/entries/<int:entry_id>/delete", methods=("GET", "POST"))
def delete_entry(entry_id):
    try:
        entry = models.Entry.get(models.Entry.get_id == entry_id)
        entry.delete_instance()
        flash("Deleted Entry", "success")
    except models.DoesNotExist:
        abort(404)
    return redirect(url_for("index"))


@app.errorhandler(404)
def abort(error):
    return render_template("404.html")


if __name__ == "__main__":
    models.initialize()
    app.run(debug=True, port=8080, host="127.0.0.1")
