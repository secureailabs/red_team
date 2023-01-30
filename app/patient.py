import json
import uuid

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.views import MethodView

from app.ai_consult import Interview
from server import db

patient_bp = Blueprint("patient_bp", __name__, template_folder="templates")


class PatientView(MethodView):
    init_every_request = False

    def __init__(
        self,
    ):
        self.patient_info = {}
        self.current_record = None

    def get(
        self,
    ):
        self.patient_info = json.loads(request.args["messages"])
        records = self.patient_info["records"]
        print(records)

        return render_template(
            "patient.html",
            patient=self.patient_info,
            records=records,
            detail=None,
            team_name="Team Red",
        )

    def post(
        self,
    ):
        show = {
            "symptoms": None,
            "diagnosis": None,
            "suggestions": None,
            "references": None,
        }
        if "consult" in request.form:
            msg = {
                "username": self.patient_info["username"],
                "age": self.patient_info["age"],
                "sex": self.patient_info["gender"],
            }
            msg = json.dumps(msg)
            return redirect(url_for("patient_bp.patient_consult", messages=msg))

        if "return" in request.form:
            self.patient_info = db.user.find_one({"username": self.patient_info["username"]})
            self.patient_info.pop("_id")
            records = self.patient_info["records"]
            return render_template(
                "patient.html",
                patient=self.patient_info,
                records=records,
                detail=None,
                show=show,
                team_name="Team Red",
            )

        if "check_record" in request.form:
            record_id = request.form["check_record"]
            self.current_record = db.record.find_one({"id": record_id})
            self.current_record.pop("_id")

        if "symptomstab" in request.form:
            show["symptoms"] = True
        elif "diagnosistab" in request.form:
            show["diagnosis"] = True
        elif "suggestionstab" in request.form:
            show["suggestions"] = True
        elif "referencestab" in request.form:
            print(self.current_record["references"][0])
            show["references"] = True

        return render_template(
            "patient.html",
            patient=self.patient_info,
            records=self.patient_info["records"],
            detail=self.current_record,
            show=show,
            team_name="Team Red",
        )


class ConsultView(MethodView):
    init_every_request = False

    def __init__(
        self,
    ):
        self.username = ""
        self.sex = ""
        self.age = 0
        self.state = {}
        self.consult = None
        self.question_num = 0
        self.id = uuid.uuid4().hex

    def get(self):
        content = {
            "text": "Please input your symptoms in English",
            "type": "text",
        }
        message = json.loads(request.args["messages"])
        self.username = message["username"]
        self.sex = message["sex"]
        self.age = int(message["age"])
        self.consult = Interview(age=self.age, sex=self.sex)
        return render_template("consult.html", team_name="Team Red", content=content)

    def post(self):
        if self.question_num > 5:
            symptoms = self.consult.get_symptom_detail()
            print(symptoms)
            conditions = self.consult.get_condition_detail()
            print(conditions)
            suggestions = self.consult.get_suggestions()
            print(suggestions)
            references = self.consult.get_references()
            consult_record = {
                "id": self.id,
                "symptoms": symptoms,
                "conditions": conditions,
                "suggestions": suggestions,
                "references": references,
            }
            db.record.insert_one(consult_record)
            db.user.find_one_and_update({"username": self.username}, {"$push": {"records": self.id}})
            return render_template("consult.html", team_name="Team Red", content=None, diagnosis=conditions)

        if "symptoms" in request.form:
            problems = request.form["symptoms"]
            self.consult.get_symptoms(problems)

        elif "single" in request.form:
            choice = request.form["single"]
            pos = choice.find("_")
            decision = choice[:pos]
            id = choice[pos + 1 :]
            new_evidence = {
                "id": id,
                "choice_id": decision,
            }
            print(new_evidence)
            self.consult.update_evidence([new_evidence])
            self.question_num += 1

        elif "group_single" in request.form:
            choice = request.form["group_single"]
            new_evidence = {
                "id": choice,
                "choice_id": "present",
            }
            print(new_evidence)
            self.consult.update_evidence([new_evidence])
            self.question_num += 1

        else:
            new_evidence = []
            for key in request.form:
                if key.startswith("s_"):
                    new_evidence.append({"id": key, "choice_id": "present"})
            print(new_evidence)
            self.consult.update_evidence(new_evidence)
            self.question_num += 1

        response = self.consult.one_turn()
        return render_template("consult.html", team_name="Team Red", content=response)


consult_view = ConsultView.as_view("patient_consult")
patient_bp.add_url_rule("/patient/consult", view_func=consult_view)
patient_view = PatientView.as_view("patient_info")
patient_bp.add_url_rule("/patient", view_func=patient_view)
