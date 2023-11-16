from flask import Flask
from flask import request, jsonify
from src.mongoQuery import add_picture

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("picture")
        text = request.values.get("text")
        latitude = float(request.values.get("latitude"))
        longitude = float(request.values.get("longitude"))
        # TODO also pass coordinates and text
        res = add_picture(file=file, latitude=latitude, longitude=longitude, text=text)
        # TODO check the res and return appropriate code
        return jsonify({"code": 201})

    except Exception as e:
        return jsonify({"code": 500, "error": e})


@app.route("/location", methods=["GET"])
def location():
    return "Hi"
