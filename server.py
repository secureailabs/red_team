from flask import Flask
from pymongo import MongoClient

server = Flask(__name__)
server.config["SESSION_TYPE"] = "memcached"
server.config["SECRET_KEY"] = "super secret key"
client = MongoClient("0.0.0.0", 27017)
db = client["project"]
collection_user = db["user"]
collection_record = db["record"]

if __name__ == "server":
    from app.dashboard import create_dashboard
    from app.pag import pag_bp
    from app.patient import patient_bp
    from app.user_manage import bp

    server.register_blueprint(bp)
    server.register_blueprint(patient_bp)
    server.register_blueprint(pag_bp)
    server = create_dashboard(server)
    server.run(debug=True, host="0.0.0.0")
