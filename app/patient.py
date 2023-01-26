import json

from flask import Blueprint, flash, redirect, render_template, request, url_for

from server import db

patient_bp = Blueprint("patient_bp", __name__, template_folder="templates")


@patient_bp.route("/patient", methods=("GET", "POST"))
def patient_info():

    patient_id = json.loads(request.args["messages"])["patient_id"]
    patient = db.user.find_one({"username": patient_id})
    records = []
    if "records" in patient:
        records = patient["records"]

    if request.method == "POST" and "consult" in request.form:
        return redirect(url_for(patient_bp.patient_consult))
    elif request.method == "POST":
        record_id = request.record
        record = db.record.find_one({"id": record_id})
        return render_template("patient.html", patient=patient, records=records, detail=record)

    return render_template("patient.html", patient=patient, records=records, detail=None)


@patient_bp.route("/patient/consult", methods=("GET", "POST"))
def patient_consult():
    if request.method == "POST":
        return render_template("consult.html")

    return render_template("consult.html")
