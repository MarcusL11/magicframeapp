from rest_framework.parsers import MultiPartParser
from django.core.files.uploadedfile import InMemoryUploadedFile
import easyocr
import numpy as np
import cv2
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from urllib.parse import quote_plus
import requests


def index(requests):

    return render(requests, 'cardapp/index.html')

class UploadImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):

        if 'file' not in request.FILES:
            return Response({'error': 'No image file provided'}, status=400)

        image_file: InMemoryUploadedFile = request.FILES['file']
        image_bytes = image_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        reader = easyocr.Reader(["en"]) 
        results = reader.readtext(img, detail = 0)
        card_name = results[0] if results else 'No text detected or recognized'

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
                    'frame_tix_price': frame_tix_price                    
                },
                status=200
            )
        else:
            return Response({'error': 'No card found'}, status=404)
        

