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

from flask import Blueprint, flash, redirect, render_template, request, url_for

from server import db

pag_bp = Blueprint("pag_bp", __name__, template_folder="templates")


@pag_bp.route("/pag", methods=("GET", "POST"))
def pag_info():
    pag_id = json.loads(request.args["messages"]).get("username")
    pag = db.user.find_one({"username": pag_id})

    return render_template("pag.html", pag=pag, team_name="Team Red")
