from PIL import Image
from transformers import pipeline

def classify_ingredients(image):
    classifier = pipeline("image-classification", model="nateraw/food101")
    results = classifier(image)
    ingredients = [result['label'] for result in results if result['score'] > 0.5]
    return ingredients



