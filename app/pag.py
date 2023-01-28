"""
 red_team
 pag.py
 
 Copyright (C) 2023 Secure Ai Labs, Inc. All Rights Reserved.
 Private and Confidential. Internal Use Only.
 
     This software contains proprietary information which shall not
     be reproduced or transferred to other documents and shall not
     be disclosed to others for any purpose without
     prior written permission of Secure Ai Labs, Inc.
 
 
"""

import json

from bson.objectid import ObjectId
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.views import MethodView

from server import db

pag_bp = Blueprint("pag_bp", __name__, template_folder="templates")


def get_list_patients():
    patient_info = db.user.find({"role": "patient"})
    list_patient = []
    for patient in patient_info:
        list_patient.append(patient)
    return list_patient


def get_patient_info(patient_id):
    patient_info = db.user.find_one({"_id": ObjectId(patient_id)})
    return patient_info


class PagView(MethodView):
    init_every_request = False

    def __init__(
        self,
    ):
        self.pag_info = {}

    def get(
        self,
    ):
        self.pag_info = json.loads(request.args["messages"])
        return render_template(
            "pag.html",
            pag=self.pag_info,
            patients=get_list_patients(),
            patient_info=None,
            team_name="Team Red",
        )

    def post(
        self,
    ):
        if "check_record" in request.form:
            patient_id = request.form["check_record"]
            patient_info = get_patient_info(patient_id)
            return render_template(
                "pag.html",
                pag=self.pag_info,
                patients=get_list_patients(),
                patient_info=patient_info,
                team_name="Team Red",
            )

        return render_template(
            "pag.html",
            pag=self.pag_info,
            patients=get_list_patients(),
            patient_info=None,
            team_name="Team Red",
        )


pag_view = PagView.as_view("pag_info")
pag_bp.add_url_rule("/pag", view_func=pag_view)


# @pag_bp.route("/pag", methods=("GET", "POST"))
# def pag_info():
#     pag_id = json.loads(request.args["messages"]).get("username")
#     pag = db.user.find_one({"username": pag_id})
#     patient_records = db.user.find({"role": "patient"})
#     list_patient = []
#     for patient in patient_records:
#         list_patient.append(patient)

#     return render_template(
#         "pag.html", pag=pag, patients=list_patient, patient_id=None, patient_records=None, team_name="Team Red"
#     )


@pag_bp.route("/pag/<id>/")
def default(id):
    # pag_id = json.loads(request.args["messages"]).get("username")
    # pag = db.user.find_one({"username": pag_id})
    # patient_records = db.user.find({"_id": id})
    return "the value is:" + id
    # return render_template(
    #     "pag.html",
    #     pag=pag,
    #     patients=get_patients_info(),
    #     patient_info=patient_records,
    #     team_name="Team Red",
    # )
