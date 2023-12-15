from google_images_search import GoogleImagesSearch
import os
import json
import random
from pymongo import MongoClient
import requests


def download_image(gis, url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save image
        with open(save_path, 'wb') as file:
            file.write(response.content)
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
    pass


def search_for_unique_image(gis, search_query, downloaded_urls, base_path, filename):
    max_attempts = 5
    attempt_urls = []

    base_search_query = f"{search_query} party people real-photo"

    for attempt in range(max_attempts):
        modified_query = f"{base_search_query} {attempt}" if attempt > 0 else base_search_query
        _search_params = {
            'q': modified_query,
            'num': 1,
            'safe': 'off',
            'fileType': 'jpg|png',
            'aspectRatio': 'tall'
        }
        gis.search(search_params=_search_params)

        if gis.results():
            image_url = gis.results()[0].url
            if image_url not in downloaded_urls:
                downloaded_urls.add(image_url)
                save_path = os.path.join(base_path, filename)
                download_image(gis, image_url, save_path)
                return True
            else:
                attempt_urls.append(image_url)

    if attempt_urls:
        chosen_url = random.choice(attempt_urls)
        downloaded_urls.add(chosen_url)
        save_path = os.path.join(base_path, filename)
        download_image(gis, chosen_url, save_path)
        return True

    return False


def load_data_into_mongodb(data):
    client = MongoClient(host="localhost", port=27017)
    db = client.locumVisiumDB
    collection = db.pictures

    # Clear the collection before inserting new data
    collection.delete_many({})

    # Now insert the new data
    collection.insert_many(data)


def load_credentials(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)


def main():
    config = load_credentials('/Users/msstudiohd/PycharmProjects/locusVisium-back-end/config.json')
    YOUR_API_KEY = config['API_KEY']
    YOUR_CSE_ID = config['CSE_ID']

    gis = GoogleImagesSearch(YOUR_API_KEY, YOUR_CSE_ID)
    downloaded_urls = set()
    base_path = '/Users/msstudiohd/PycharmProjects/locusVisium-back-end/data'

    file_path = '/Users/msstudiohd/PycharmProjects/locusVisium-back-end/src/mock_data.json'  # Replace with your actual file path
    with open(file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        filename = os.path.basename(item['path'])
        tags = item['tags']
        modified_tags = [
            'welcoming place' if tag == 'CozyPlace' else
            'event party' if tag == 'Event' else tag
            for tag in tags
        ]
        title_tags = f"{' '.join(modified_tags)}"
        search_for_unique_image(gis, title_tags, downloaded_urls, base_path, filename)

    load_data_into_mongodb(data)


if __name__ == "__main__":
    main()
