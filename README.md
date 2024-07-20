# LocumVisium Back-end
<img src="gitData/ic_launcher.webp" alt="Locum Visum Logo" width="170" height="170">

Locum Visium is a community-based social media Android app designed to help users discover popular local places and events near their position. 📍📱

## Overview 
# LocumVisium Back-end
<img src="gitData/Locum%20Visium.gif" alt="overview gif" width="375" height="674">

[Overview Video](https://www.youtube.com/watch?v=UocxDTZqIPg&ab_channel=MSstudioHD)

## Features
- **Discover** Local Places and Events: Easily find popular local spots and events through user-generated content.
- **Share** Your Favorite Spots: Take and share pictures and text about your favorite places, increasing their visibility.
- **Interactive Map**: Posts are displayed on an interactive map using the Google Maps API, with clickable pins for easy exploration. 
- **Social Media Feed**: View posts in a social media-like scroll-feed, showcasing pictures and descriptions of local spots.

## Technologies
- **Android API 31**: application written in Java 
- **Google Maps API**: Used to display an interactive map with clickable pins. 
- **GoogleImagesSearch API**: To retrieve images for the mock data.
- Android Camera and GPS Integration
- **Backend Server**: Developed using Python with Flask.

   Here's the revised version of the installation and usage guide, with improved clarity and grammar:

## Android App git 
[Android app git](https://github.com/JacobSalvi/mwc-project)


## Installation
Create a virtual environment:
```shell
python3 -m venv ./.venv
```

Activate the virtual environment:
```shell
source .venv/bin/activate
```

Install required packages:
```shell
python3 -m pip install -r requirements.txt
```

## Database Setup
Ensure MongoDB is running locally on port 27017.

### Load Mock Data into MongoDB
Execute the script **src/database_creator.py** to import the data from the file `mock_data_2.json` into MongoDB.

### [Optional] Image Retrieval Functionality
The script **src/database_creator.py** includes functionality to retrieve images using the Google Images Search API, which was utilized to generate the mock data. To use this feature, you must provide your API keys as follows:

- Set `YOUR_API_KEY` to your Google API key.
- Set `YOUR_CSE_ID` to your Custom Search Engine ID.

Here's an improved version of the instruction to run the application:

## Running the Application
To start the application, execute the script **main.py**:

```shell
python main.py
```
