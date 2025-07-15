import requests

def generate_recipe(ingredients):
    prompt = (
        f"Generate a healthy recipe using the following ingredients: {', '.join(ingredients)}. "
        "Include ingredients list and step-by-step instructions."
    )
    return None #placeholder for gpt or llama response

def get_nutrition_info(ingredients):
    url = "https://api.edamam.com/api/nutrition-data"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "title": "Meal Buddy",
        "ingr": ingredients
    }
    params = {
        "app_id": "REPLACE THIS", 
        "app_key": "REPLACE THIS"
        
    }
    response = requests.post(url, headers=headers, json = body, params=params)

    if response.status_code == 200:
        return response.json()
    return None

def call_model():
    pass