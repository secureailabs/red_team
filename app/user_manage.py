from uuid import uuid4

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from server import db

bp = Blueprint("bp", __name__, template_folder="templates")


@bp.route("/")
def index():
    return "Home route."


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = db.user.find_one({"username": username})
        error = None

        print(user, flush=True)
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        if error is None:
            if user["role"] == "pag":
                return redirect(url_for("pag"))
            else:
                return redirect(url_for("patient"))

        flash(error)

    return render_template("login.html")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        if request.form["choice"] == "patient":
            return redirect(url_for("bp.register_patient"))
        elif request.form["choice"] == "PAG":
            return redirect(url_for("bp.register_pag"))

    return render_template("register.html")


@bp.route("/register/pag", methods=("GET", "POST"))
def register_pag():
    if request.method == "POST":
        error = None
        register_info = {}

        register_info["username"] = request.form["username"]
        register_info["password"] = request.form["password"]
        register_info["email"] = request.form["email"]
        register_info["disease"] = request.form["disease"]
        register_info["role"] = "pag"

        # to do: username/email duplication, password complexity
        if not register_info["username"]:
            error = "username can not be empty"
        elif not register_info["password"]:
            error = "password can not be empty"
        elif not register_info["email"]:
            error = "need to provide an email"
        elif not register_info["disease"]:
            error = "need to specify disease focus"

        if error is None:
            register_info["password"] = generate_password_hash(register_info["password"])
            db.user.insert_one(register_info)

    return render_template("pag_register.html")


@bp.route("/register/patient", methods=("GET", "POST"))
def register_patient():
    if request.method == "POST":
        error = None
        register_info = {}

        register_info["username"] = request.form["username"]
        register_info["password"] = request.form["password"]
        register_info["email"] = request.form["email"]
        register_info["age"] = request.form["age"]
        register_info["gender"] = request.form["gender"]
        register_info["height"] = request.form["height"]
        register_info["weight"] = request.form["weight"]
        register_info["bloodtype"] = request.form["bloodtype"]
        register_info["role"] = "patient"

        if not register_info["username"]:
            error = "username can not be empty"
        elif not register_info["password"]:
            error = "password can not be empty"
        elif not register_info["email"]:
            error = "need to provide an email"

        if error is None:
            register_info["password"] = generate_password_hash(register_info["password"])
            db.user.insert_one(register_info)

    return render_template("patient_register.html")
