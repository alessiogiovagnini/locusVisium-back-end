from pathlib import Path
from pymongo import MongoClient
import datetime
import random, string, base64

client = MongoClient(host="localhost", port=27017)
db = client.locumVisiumDB
collection = db.pictures


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def add_picture(file, longitude: float, latitude: float, text: str):
    path: Path = Path(f"data/{randomword(10)}-{datetime.datetime.now()}.png")

    decoded: bytes = base64.b64decode(file)
    with open(path, 'wb') as output_file:
        output_file.write(decoded)

    mongo_object = {
        "path": path.as_posix(),
        "text": text,
        "location": {
            "type": "Point",
            "coordinates": [longitude, latitude]
        }
    }
    res = collection.insert_one(mongo_object)
    return res


# TODO return pictures based on coordinates
def get_pictures(longitude: float, latitude: float, max_distance: float):
    # geoJson query
    res = collection.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$minDistance": 0,
                "$maxDistance": max_distance
            }
        }
    }, {"_id": 0})  # the object Id is not serializable in the response, so this exclude it from the returned values
    return [el for el in res]


def get_single_picture(longitude: float, latitude: float):
    res = collection.find_one({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$minDistance": 0,
                "$maxDistance": 1000
            }
        }
    }, {"_id": 0})
    return res


# create an index to retrieve coordinates
def make_index():
    collection.create_index({"location": "2dsphere"})
