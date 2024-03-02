import os
import base64
import json
from google.oauth2 import service_account
from google.cloud import vision
from dotenv import load_dotenv

dotenv_path = '../mtgproject/.env'
load_dotenv(dotenv_path=dotenv_path)

def detect_text(path):
    encoded_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_BASE64')
    if not encoded_credentials:
        raise Exception('GOOGLE_APPLICATION_CREDENTIALS_BASE64 environment variable not set')
    
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(decoded_credentials)
    )

    client = vision.ImageAnnotatorClient(credentials=credentials)

    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    card_name = response.text_annotations[0].description.split('\n')[0]

    print('Name:')
    print(card_name)

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(response.error.message))

# Example usage:
detect_text('../theme/static/images/testcard4.jpg')
