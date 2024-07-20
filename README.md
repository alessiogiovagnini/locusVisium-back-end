# LocumVisium Back-end
<img src="gitData/ic_launcher.webp" alt="Locum Visum Logo" width="170" height="170">

Locum Visium is a community-based social media Android app designed to help users discover popular local places and events near their position. 📍📱

## Overview 
# LocumVisium Back-end
<img src="gitData/Locum%20Visium.gif" alt="overview gif" width="500" height="700">

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

## Installation
make virtual env
```shell
python3 -m venv ./.venv
```

# activate virtual environment
```shell
source .venv/bin/activate
```

install requirement
```shell
python3 -m pip install -r requirements.txt
```

# Database
you need mongodb running on localhost on port: 27017. 
