import json
from uuid import uuid4

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from server import db

bp = Blueprint("bp", __name__, template_folder="templates")


# PAG page
@bp.route("/", methods=("GET", "POST"))
@bp.route("/home")
def home():
    if request.method == "POST" and "choice" in request.form:
        return redirect(url_for("bp.login"))
    return render_template("default_template.html", team_name="Team Red")


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
                pag_info = json.dumps({"pag_id": username})
                return redirect(url_for("pag_bp.pag_info", messages=pag_info))
            else:
                patient_info = json.dumps({"patient_id": username})
                return redirect(url_for("patient_bp.patient_info", messages=patient_info))

        flash(error)

    return render_template("login.html", team_name="Team Red")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        if request.form["choice"] == "Register Patient":
            return redirect(url_for("bp.register_patient"))
        elif request.form["choice"] == "Register PAG":
            return redirect(url_for("bp.register_pag"))

    return render_template("register.html", team_name="Team Red")


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
            return redirect(url_for("bp.login"))
    return render_template("pag_register.html", team_name="Team Red")


@bp.route("/register/patient", methods=("GET", "POST"))
def register_patient():
    if request.method == "POST":
        error = None
        register_info = {}

        register_info["username"] = request.form["username"]
        register_info["password"] = request.form["password"]
        register_info["email"] = request.form["email"]
        register_info["firstname"] = request.form["firstname"]
        register_info["lastname"] = request.form["lastname"]
        register_info["address"] = request.form["address"]
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
            return redirect(url_for("bp.login"))

    return render_template("patient_register.html", team_name="Team Red")
