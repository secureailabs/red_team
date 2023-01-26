from flask import Flask
from pymongo import MongoClient

server = Flask(__name__)
server.config["SESSION_TYPE"] = "memcached"
server.config["SECRET_KEY"] = "super secret key"
client = MongoClient("localhost", 27017)
db = client["project"]
collection_user = db["user"]
collection_record = db["record"]


if __name__ == "server":
    from app.patient import patient_bp
    from app.user_manage import bp

    server.register_blueprint(bp)
    server.register_blueprint(patient_bp)
    server.run(debug=True)
