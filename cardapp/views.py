from google.oauth2 import service_account
from google.cloud import vision
import base64
import json
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import quote_plus
import requests
from django.shortcuts import render
from mtgproject.settings import ENCODED_CREDENTIALS as encoded_credentials



def index(requests):

    return render(requests, 'cardapp/index.html')

class UploadImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):        

        if 'file' not in request.FILES:
            return Response({'error': 'No image file provided'}, status=400)
        
        if encoded_credentials is None:
            raise Exception('GOOGLE_APPLICATION_CREDENTIALS_BASE64 environment variable not set')
        
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(decoded_credentials)
        )

        client = vision.ImageAnnotatorClient(credentials=credentials)
        
        image_file = request.FILES.get('file')
        if image_file is None:
            return Response({'error': 'No image file provided'}, status=400)
        
        content = image_file.read()        
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        text = response.text_annotations
        card_name = text[0].description.split('\n')[0] if response else 'No text detected or recognized'
                    
        encoded_card_name = quote_plus(card_name)
        scryfall_api_url = f'https://api.scryfall.com/cards/named?fuzzy={encoded_card_name}'
        fetch_data = requests.get(scryfall_api_url)
    
        if fetch_data.status_code == 200:
            fetch_data_json = fetch_data.json()
            pricing = fetch_data_json.get("prices", {})

            frame_usd_price = pricing.get("usd", "")
            frame_usd_foil_price = pricing.get("usd_foil", "")
            frame_usd_etched_price = pricing.get("usd_etched", "")
            frame_eur_price = pricing.get("eur", "")
            frame_eur_foil_price = pricing.get("eur_foil", "")
            frame_tix_price = pricing.get("tix", "")
            
            # fetch rulings
            rulings_api_url = fetch_data_json.get("rulings_uri", "")            
            fetch_rulings = requests.get(rulings_api_url)
            fetch_rulings_json = fetch_rulings.json()        
            
            frame_card_rulings =[]
            
            for data in fetch_rulings_json.get("data", []):
                publish_at = data.get("published_at", "")
                comment = data.get("comment", "")
                
                frame_card_rulings.append(
                    {
                        'publish_at': publish_at,
                        'comment': comment
                    }
                )        
            
            frame_card_name = fetch_data_json.get("name", "No card found")
            
            frame_card_image = fetch_data_json.get("image_uris", {}).get("normal", "")

            frame_tcg_purcase_link = fetch_data_json.get("purchase_uris", {}).get("tcgplayer", "")
            
            return Response(
                {
                    'frame_card_name': frame_card_name,
                    'frame_card_image': frame_card_image,
                    'frame_card_rulings': frame_card_rulings,
                    'frame_usd_price': frame_usd_price,
                    'frame_usd_foil_price': frame_usd_foil_price,
                    'frame_usd_etched_price': frame_usd_etched_price,
                    'frame_eur_price': frame_eur_price,
                    'frame_eur_foil_price': frame_eur_foil_price,
                    'frame_tix_price': frame_tix_price,
                    'frame_tcg_purcase_link': frame_tcg_purcase_link                    
                },
                status=200
            )
        else:
            return Response({'error': 'No card found'}, status=404)
        

