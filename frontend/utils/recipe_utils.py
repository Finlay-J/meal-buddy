import requests
from transformers import FlaxAutoModelForSeq2SeqLM
from transformers import AutoTokenizer

def generate_recipe(ingredients):
    try:
        # Handle both string and list inputs
        if isinstance(ingredients, str):
            ingredients_text = ingredients
        else:
            ingredients_text = ", ".join(ingredients)
        
        print(f"Debug - ingredients input: {ingredients}")
        print(f"Debug - ingredients_text: {ingredients_text}")
        
        # Use the model to generate recipe
        generated_recipes = generation_function(ingredients_text)
        
        if generated_recipes and len(generated_recipes) > 0:
            return generated_recipes[0]
        else:
            return f"Recipe using {ingredients_text}: This is a placeholder recipe."
    except Exception as e:
        print(f"Error generating recipe: {e}")
        ingredients_text = ingredients if isinstance(ingredients, str) else ", ".join(ingredients)
        return f"Recipe using {ingredients_text}: This is a placeholder recipe."

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



MODEL_NAME_OR_PATH = "flax-community/t5-recipe-generation"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_OR_PATH, use_fast=True)
model = FlaxAutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME_OR_PATH)

prefix = "items: "
generation_kwargs = {
    "max_length": 512,
    "min_length": 64,
    "no_repeat_ngram_size": 3,
    "early_stopping": True,
    "num_beams": 4,  # Changed from 5 to 4
    "length_penalty": 1.5,
}


special_tokens = tokenizer.all_special_tokens
tokens_map = {
    "<sep>": "--",
    "<section>": "\n"
}
def skip_special_tokens(text, special_tokens):
    for token in special_tokens:
        text = text.replace(token, "")

    return text

def target_postprocessing(texts, special_tokens):
    if not isinstance(texts, list):
        texts = [texts]
    
    new_texts = []
    for text in texts:
        text = skip_special_tokens(text, special_tokens)

        for k, v in tokens_map.items():
            text = text.replace(k, v)

        new_texts.append(text)

    return new_texts

def generation_function(texts):
    _inputs = texts if isinstance(texts, list) else [texts]
    inputs = [prefix + inp for inp in _inputs]
    
    print(f"Debug - _inputs: {_inputs}")
    print(f"Debug - inputs after prefix: {inputs}")
    
    inputs = tokenizer(
        inputs, 
        max_length=256, 
        padding="max_length", 
        truncation=True, 
        return_tensors="jax"
    )

    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask
    
    print(f"Debug - input_ids shape: {input_ids.shape}")
    print(f"Debug - attention_mask shape: {attention_mask.shape}")

    try:
        # Try with simpler parameters first
        simple_kwargs = {
            "max_length": 256,
            "min_length": 32,
            "do_sample": False,
            "num_beams": 1,  # Greedy decoding
        }
        
        output_ids = model.generate(
            input_ids=input_ids, 
            attention_mask=attention_mask,
            **simple_kwargs
        )
        generated = output_ids.sequences
        print(f"Debug - generated shape: {generated.shape}")
        generated_recipe = target_postprocessing(
            tokenizer.batch_decode(generated, skip_special_tokens=False),
            special_tokens
        )
        return generated_recipe
    except Exception as e:
        print(f"Error in generation: {e}")
        print(f"Error type: {type(e)}")
        # Create a structured fallback recipe
        ingredients_text = ', '.join(_inputs)
        fallback_recipe = f"title: Recipe with {ingredients_text}\n\ningredients: {ingredients_text} -- salt -- pepper -- olive oil\n\ndirections: Cook the {ingredients_text} with seasonings until done -- Serve hot"
        return [fallback_recipe]

