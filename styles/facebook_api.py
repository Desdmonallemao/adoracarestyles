import requests

def post_to_facebook(page_id, access_token, message, image_path):
    url = f"https://graph.facebook.com/{page_id}/photos"
    files = {'source': open(image_path, 'rb')}
    data = {
        'access_token': access_token,
        'message': message,
    }
    response = requests.post(url, files=files, data=data)
    return response.json()
