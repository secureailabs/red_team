from flask import Flask
from pymongo import MongoClient

server = Flask(__name__)
client = MongoClient("localhost", 27017)
db = client["project"]
collection = db["user"]


if __name__ == "server":
    from app.user_manage import bp

    server.register_blueprint(bp)
    server.run(debug=True)
