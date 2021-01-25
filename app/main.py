import os
from flask import Flask, render_template, request
import requests
import random
import secrets

app=Flask(__name__)

def get_background(location):
    """
    Gets semi-randomized background image for a location.
    Uses the Unsplash API to get the JSON object of the image.

    Args:
        location: Name of location as user input in the Home page.

    Returns:
        image_path: URL to the image.
        image_color: The primary color of the image according to the API.
        image_author: The name of the photographer.
        author_profile: The URL to the photographer's profile.
    """

    unsplash_id = 'cCDZL9dbBhk86Gr0z1x2BJWfN8Fo04oS0X3rZSW3Nk0'
    unsplash_url = 'https://api.unsplash.com/search/photos'
    
    # Optional params 'page' and 'per_page':
    # 'page': defines which page to retrieve (default 1)
    # 'per_page': defines how many items to retrieve in each page (default 10, max 30)
    # See API documentation, section Pagination
    per_page = 30
    obj = requests.get(unsplash_url, 
            params={'client_id': unsplash_id, 'per_page': per_page, 'query': location, 'orientation': 'landscape'}).json()

    total_pages = obj['total_pages']
    total_images = obj['total']
    num_page = max(1, secrets.randbelow(total_pages))
    num_images_last_page = total_images - per_page * (total_pages - 1)

    if num_page == total_pages:
        photo_id = max(1, secrets.randbelow(num_images_last_page))
    else:
        photo_id = max(1, secrets.randbelow(per_page))

    image_path = obj['results'][photo_id]['urls']['small']
    image_color = obj['results'][photo_id]['color']
    image_author = obj['results'][photo_id]['user']['name']
    author_profile = obj['results'][photo_id]['user']['links']['self']
    return image_path, image_color, image_author, author_profile

def get_location_object(location):
    """
    Gets weather information JSON object for a location.
    Uses the OpenWeatherMap API.

    Args:
        location: Name of location as user input in the Home page.
    
    Returns:
        loc_obj: JSON object containing weather information.
    """

    owm_id = '4bb3c583ee24c1173486edeb1649a47f'
    owm_url = 'http://api.openweathermap.org/data/2.5/weather?q='
    complete_path = owm_url + location + '&appid=' + owm_id + '&units=metric'
    loc_obj = requests.get(complete_path).json()
    return loc_obj

def check_valid_location(loc_obj):
    """
    Checks if information for the input location is available.

    Args:
        loc_obj: JSON object of the location.

    Returns:
        False: if the location is not valid ("cod" code of "404").
        True: if otherwise.
    """

    if loc_obj['cod'] != '404':
        return True
    return False

def get_weather_info(loc_obj):
    """
    Gets weather information from JSON object of valid input location.

    Args:
        loc_obj: JSON object of location.

    Returns:
        description: general description of weather, will serve as caption.
        icon_url: URL to corresponding weather icon.
        temp: current temperature.
    """
    description = loc_obj['weather'][0]['description'].capitalize()

    # Weather conditions details: https://openweathermap.org/weather-conditions
    icon_id = loc_obj['weather'][0]['icon']
    icon_base_url = 'http://openweathermap.org/img/wn/'
    icon_url = icon_base_url + icon_id + '@2x.png'

    temp = loc_obj['main']['temp']

    return description, icon_url, temp


@app.route('/')
def hello():
    """
    Renders the home page containing input field.

    Args:
        None.
    
    Returns:
        Renders the home page HTML template.
    """
    image_path, image_color, image_author, author_profile = get_background('nature')
    return render_template('home.html', image_path = image_path, image_color = image_color,
                                        image_author = image_author, author_profile = author_profile)

@app.route('/weather')
def weather():
    """
    Renders the weather information page of input location.

    Args:
        None.

    Returns:
        Renders the weather page HTML template if location is valid.
        Renders the not found page HTML template if location is invalid/unavailable.
    """
    location = request.args.get('location', '')
    loc_obj = get_location_object(location)

    if not check_valid_location(loc_obj):
        image_path, image_color, image_author, author_profile = get_background('nature')
        return render_template('not_found.html', image_path = image_path, image_color = image_color, 
                                            image_author = image_author, author_profile = author_profile)

    image_path, image_color, image_author, author_profile = get_background(location)
    description, icon_url, temp = get_weather_info(loc_obj)
    return render_template('weather.html', location = location.title(), image_path = image_path, image_color = image_color,
                                        image_author = image_author, author_profile = author_profile,
                                        description = description, icon_url = icon_url, temp = temp)