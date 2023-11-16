from flask import Flask
from flask import request, jsonify
from mongoQuery import add_picture

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("picture")
    # TODO also pass coordinates and text
    res = add_picture(file=file)
    # TODO check the res and return appropriate code
    return jsonify({"code": 201})


@app.route("/location", methods=["GET"])
def location():
    return "Hi"
