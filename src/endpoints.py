from flask import Flask
from flask import request, jsonify
from pymongo import MongoClient
import datetime
from pathlib import Path

app = Flask(__name__)
client = MongoClient(host="localhost", port=27017)
db = client.locumVisiumDB


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("picture")
    path: Path = Path(f"data/{file.name}-{datetime.datetime.now()}.png")
    file.save(dst=path.absolute())
    collection = db.pictures
    collection.insert_one({"path": path.as_posix()})
    return jsonify({"code": 201})


@app.route("/location", methods=["GET"])
def location():
    return "Hi"
