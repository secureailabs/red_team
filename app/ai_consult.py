import time
import xml.etree.ElementTree as ET
from urllib.parse import quote

import infermedica_api
import openai
import requests

id = "3fac8098"
key = "a3aac776cb9346d6e06933aad49e87e1"
gpt_org_id = "org-doZGGQVXBA2x6USqxs1C2xwi"
gpt_key = "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"
openai.organization = gpt_org_id
openai.api_key = gpt_key


class Interview:
    def __init__(
        self,
        age,
        sex,
    ):
        self.sex = sex
        self.age = age
        self.api = infermedica_api.APIv3Connector(app_id=id, app_key=key)
        self.evidence = []
        self.state = {}

    def get_symptoms(self, problems):
        response = self.api.parse(text=problems, age=self.age)
        for symptom in response["mentions"]:
            new_evidence = {
                "id": symptom["id"],
                "choice_id": symptom["choice_id"],
            }
            self.evidence.append(new_evidence)

    def update_evidence(
        self,
        new_evidences,
    ):
        for e in new_evidences:
            self.evidence.append(e)

    def one_turn(
        self,
    ):
        self.state = self.api.diagnosis(evidence=self.evidence, age=self.age, sex=self.sex)
        return self.state["question"]

    def get_diagnosis(
        self,
    ):
        return self.state

    def get_symptom_detail(
        self,
    ):
        info = []
        for symptom in self.evidence:
            if symptom["id"].startswith("s_"):
                i = self.api.symptom_details(symptom_id=symptom["id"], age=self.age)
                info.append(i["name"])
        return info

    def get_condition_detail(
        self,
    ):
        info = []
        for condition in self.state["conditions"]:
            condition_detail = self.api.condition_details(condition_id=condition["id"], age=self.age)
            entry = {
                "name": condition_detail["name"],
                "categories": condition_detail["categories"],
                "prevalence": condition_detail["prevalence"],
                "severity": condition_detail["severity"],
                "probability": condition["probability"],
            }
            info.append(entry)
        return info

    def get_suggestions(
        self,
    ):
        info = {}
        for condition in self.state["conditions"]:
            condition_name = condition["name"]
            question = f"What medication and treatment should I use for {condition_name}?"
            response = openai.Completion.create(engine="text-davinci-003", prompt=question, max_tokens=500)
            info[condition_name] = response.to_dict_recursive()["choices"][0]["text"]
        return info

    def get_references(
        self,
    ):
        condition = self.state["conditions"][0]["name"]
        pubmed_endpoint = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        query_str = "?db=pubmed&term=" + quote(condition)
        response = requests.get(pubmed_endpoint + query_str)
        root = ET.fromstring(response.text)
        idlist = []
        for elem in root.iter("Id"):
            id = elem.text
            idlist.append(id)
        pubmed_endpoint = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        reference_list = []
        for id in idlist:
            query_str = "?db=pubmed&id=" + id + "&retmode=json"
            response = requests.get(pubmed_endpoint + query_str)
            response = response.json()
            article_info = response["result"][id]
            if article_info["elocationid"] == "":
                article_info.pop("elocationid")
            else:
                article_info["elocationid"] = article_info["elocationid"][5:]
            reference_list.append(article_info)
            time.sleep(1)
        return reference_list
