# DOCUMENTATION: https://www.jaided.ai/easyocr/documentation/

import easyocr


def extract_card_name(image_path):
    reader = easyocr.Reader(["en"])  # Assuming card names are in English
    results = reader.readtext(image_path, detail = 0)
    card_name = results[0]

    return card_name    