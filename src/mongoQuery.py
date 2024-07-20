import base64
import datetime
import random
import string
from pathlib import Path

from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)
db = client.locumVisiumDB
collection = db.pictures


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def add_picture(file, longitude: float, latitude: float, description: str, title: str, tags: list[str], provider: str):
    path: Path = Path(f"data/{randomword(10)}-{datetime.datetime.now()}.png")

    decoded: bytes = base64.b64decode(file)
    with open(path, 'wb') as output_file:
        output_file.write(decoded)

    mongo_object = {
        "path": path.as_posix(),
        "description": description,
        "title": title,
        "tags": tags,
        "provider": provider,
        "location": {
            "type": "Point",
            "coordinates": [longitude, latitude]
        }
    }
    res = collection.insert_one(mongo_object)
    return res


# TODO return pictures based on coordinates
def get_pictures(longitude: float, latitude: float, max_distance: float, tags: list[str] = []):
    # geoJson query
    # the object Id is not serializable in the response, so this excludes it from the returned values
    filter: dict = {
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
    }
    #filter = {}
    if len(tags) != 0:
        filter["tags"] = {"$all": tags}
    res = collection.find(filter=filter, projection={"_id": 0})
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
