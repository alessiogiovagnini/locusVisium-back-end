from flask import Flask
from flask import request, jsonify
from src.mongoQuery import add_picture, get_pictures
import base64

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.values.get("picture")
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
    try:
        latitude = float(request.values.get("latitude"))
        longitude = float(request.values.get("longitude"))
        max_distance = float(request.values.get("max"))
        res = get_pictures(longitude=longitude, latitude=latitude, max_distance=max_distance)

        files: dict = {}
        for pic in res:
            file = open(pic.get("path"), "rb")
            files[pic.get("path")] = str(base64.b64encode(file.read()))

        return jsonify({"code": 200, "data": res, "files": files})
    except Exception as e:
        return jsonify({"code": 500, "error": e})


@app.route("/", methods=["GET"])
def ping():
    return "pong"
