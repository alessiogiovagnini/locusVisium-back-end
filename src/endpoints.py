from flask import Flask
from flask import request, jsonify
from src.mongoQuery import add_picture, get_pictures

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
    try:
        latitude = float(request.values.get("latitude"))
        longitude = float(request.values.get("longitude"))
        max_distance = float(request.values.get("max"))
        res = get_pictures(longitude=longitude, latitude=latitude, max_distance=max_distance)
        # TODO get the actual image data and return everything
        print(res)
        return jsonify({"code": 200})
    except Exception as e:
        return jsonify({"code": 500, "error": e})
