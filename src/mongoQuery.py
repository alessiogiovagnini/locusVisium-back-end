from pathlib import Path
from pymongo import MongoClient
import datetime

client = MongoClient(host="localhost", port=27017)
db = client.locumVisiumDB
collection = db.pictures


# TODO save picture with text
def add_picture(file, longitude: float, latitude: float, text: str):
    path: Path = Path(f"data/{file.name}-{datetime.datetime.now()}.png")
    file.save(dst=path.absolute())

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
    })
    return res


