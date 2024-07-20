import json
from functools import wraps
from http import HTTPStatus

from flask import Flask, abort, Response
from flask import request, jsonify
from src.mongoQuery import add_picture, get_pictures, get_single_picture
import base64

app = Flask(__name__)


def ensure_required_fields_are_filled(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.values.get("picture"):
            return abort(HTTPStatus.BAD_REQUEST, "Missing field picture")
        if not request.values.get("description"):
            return abort(HTTPStatus.BAD_REQUEST, "Missing field description")
        if not request.values.get("title"):
            return abort(HTTPStatus.BAD_REQUEST, "Missing field title")
        return f(*args, **kwargs)
    return decorated


# upload a picture to the server
@app.route("/upload", methods=["POST"])
@ensure_required_fields_are_filled
def upload():
    try:
        file: str = request.values.get("picture")
        description: str = request.values.get("description")
        latitude: float = float(request.values.get("latitude"))
        longitude: float = float(request.values.get("longitude"))
        tags: list[str] = json.loads(request.values.get("tags")) if request.values.get("tags") else []
        title: str = request.values.get("title")
        provider: str = request.values.get("provider")
        res = add_picture(file=file, latitude=latitude, longitude=longitude, description=description, title=title, tags=tags, provider=provider)
        # TODO check the res and return appropriate code
        return Response("File uploaded successfully", status=HTTPStatus.OK)
    except Exception as e:
        print(e)
        return Response("File couldn't be uploaded because of a server error", status=HTTPStatus.INTERNAL_SERVER_ERROR)


# get all picture info and files in a certain radius from a location
@app.route("/locations", methods=["GET"])
def locations():
    try:
        latitude = float(request.args.get("latitude"))
        longitude = float(request.args.get("longitude"))
        max_distance = float(request.args.get("max"))
        tags: list[str] = json.loads(request.values.get("tags")) if request.values.get("tags") else []
        if not latitude or not longitude or not max_distance:
            return jsonify({"code": 400})
        res = get_pictures(longitude=longitude, latitude=latitude, max_distance=max_distance, tags=tags)

        files: dict = {}
        for pic in res:
            file = open(pic.get("path"), "rb")
            files[pic.get("path")] = base64.b64encode(file.read()).decode("ascii")

        return jsonify({"code": 200, "data": res})
    except Exception as e:
        return jsonify({"code": 500, "error": e})


# get a single picture from a position, return the closest picture in a radius of 1 km
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


# get the file from a path
@app.route("/picture", methods=["GET"])
def get_picture():
    try:

        path: str = request.args.get("path")
        file = open(path, "rb")
        file_64 = base64.b64encode(file.read()).decode("ascii")

        return jsonify({"code": 200, "file": file_64})

    except Exception as e:
        return jsonify({"code": 500, "error": e })


# get metadata of all pictures in a radius
@app.route("/information", methods=["GET"])
def locations_information():
    try:
        latitude = float(request.args.get("latitude"))
        longitude = float(request.args.get("longitude"))
        max_distance = float(request.args.get("max"))
        tags: list[str] = json.loads(request.values.get("tags")) if request.values.get("tags") else []
        if not latitude or not longitude or not max_distance:
            return jsonify({"code": 400})
        res = get_pictures(longitude=longitude, latitude=latitude, max_distance=max_distance, tags=tags)

        return jsonify({"code": 200, "data": res})
    except Exception as e:
        return jsonify({"code": 500, "error": e})


@app.route("/", methods=["GET"])
def ping():
    return "pong"
