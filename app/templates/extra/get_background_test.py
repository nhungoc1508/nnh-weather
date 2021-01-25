import requests, random

def get_background(location):
    """
    Gets semi-randomized background image for a location.
    Uses the Unsplash API to get the JSON object of the image.

    Args:
        location: Name of location as user input in the Home page.

    Returns:
        image_path: URL to the image.
        image_color: The primary color of the image according to the API.
    """

    unsplash_id = 'cCDZL9dbBhk86Gr0z1x2BJWfN8Fo04oS0X3rZSW3Nk0'
    unsplash_url = 'https://api.unsplash.com/search/photos'

    per_page = 30
    obj = requests.get(unsplash_url, 
            params={'client_id': unsplash_id, 'per_page': per_page, 'query': location, 'orientation': 'landscape'}).json()
    total_pages = obj['total_pages']
    total_images = obj['total']
    print('Total pages: ', total_pages)
    print('Total images: ', total_images)
    num_page = random.randint(1, min(10, total_pages))
    print('Num page: ', num_page)
    num_images_last_page = total_images - per_page * (total_pages - 1)
    photo_id = random.randint(0, min(per_page - 1, num_images_last_page - 1))
    print('Photo ID:', photo_id)
    print('Len obj: ', len(obj['results']))
    image_path = obj['results'][photo_id]['urls']['regular']
    image_color = obj['results'][photo_id]['color']
    print(image_path)

get_background('Chongqing')