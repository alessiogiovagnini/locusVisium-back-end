from flask import Flask
from flask import request, jsonify
from src.mongoQuery import add_picture, get_pictures, get_single_picture
import base64

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.values.get("picture")
        text = request.values.get("text")
        latitude = float(request.values.get("latitude"))
        longitude = float(request.values.get("longitude"))
        if not file or not text or not latitude or not longitude:
            return jsonify({"code": 400})
        res = add_picture(file=file, latitude=latitude, longitude=longitude, text=text)
        # TODO check the res and return appropriate code
        return jsonify({"code": 201})

    except Exception as e:
        return jsonify({"code": 500, "error": e})


@app.route("/locations", methods=["GET"])
def locations():
    try:
        latitude = float(request.args.get("latitude"))
        longitude = float(request.args.get("longitude"))
        max_distance = float(request.args.get("max"))
        if not latitude or not longitude or not max_distance:
            return jsonify({"code": 400})
        res = get_pictures(longitude=longitude, latitude=latitude, max_distance=max_distance)

        files: dict = {}
        for pic in res:
            file = open(pic.get("path"), "rb")
            files[pic.get("path")] = base64.b64encode(file.read()).decode("ascii")

        return jsonify({"code": 200, "data": res, "files": files})
    except Exception as e:
        return jsonify({"code": 500, "error": e})


@app.route("/location", methods=["GET"])
def location():
    try:
        latitude = float(request.args.get("latitude"))
        longitude = float(request.args.get("longitude"))
        if not latitude or not longitude:
            return jsonify({"code": 400})

        res = get_single_picture(longitude=longitude, latitude=latitude)
        if not res:
            return jsonify({"code": 404})
        file = open(res.get("path"), "rb")
        file_64 = base64.b64encode(file.read()).decode("ascii")

        return jsonify({"code": 200, "data": res, "file": file_64})
    except Exception as e:
        return jsonify({"code": 500, "error": e})


@app.route("/picture", methods=["GET"])
def get_picture():
    try:

        path: str = request.args.get("path")
        file = open(path, "rb")
        file_64 = base64.b64encode(file.read()).decode("ascii")

        return jsonify({"code": 200, "file": file_64})

    except Exception as e:
        return jsonify({"code": 500, "error": e })


@app.route("/information", methods=["GET"])
def locations_information():
    try:
        latitude = float(request.args.get("latitude"))
        longitude = float(request.args.get("longitude"))
        max_distance = float(request.args.get("max"))
        if not latitude or not longitude or not max_distance:
            return jsonify({"code": 400})
        res = get_pictures(longitude=longitude, latitude=latitude, max_distance=max_distance)

        return jsonify({"code": 200, "data": res})
    except Exception as e:
        return jsonify({"code": 500, "error": e})


@app.route("/", methods=["GET"])
def ping():
    return "pong"
