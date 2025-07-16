import streamlit as st
from utils.image_utils import classify_ingredients
from utils.recipe_utils import generate_recipe, get_nutrition_info, generation_function



st.set_page_config(page_title="Meal Buddy", 
                   page_icon="🍽️",
                   layout="centered")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        color: #2E2E2E;
        background-color: #FAF9F6;
    }

    h1, h2, h3 {
        color: #4CAF50;
    }

    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
    }

    .stButton > button:hover {
        background-color: #45a049;
    }

    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #2E2E2E;
        border-radius: 5px;
    }

    .stFileUploader {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Meal Buddy 🍽️")
st.write("Welcome to Meal Buddy! Upload an image of your ingredients, and we'll help you create a delicious recipe.")

tab1, tab2 = st.tabs(["Upload Ingredients", "Upload Image"])

ingredients = []

with tab1:
    st.header("Upload Ingredients")
    ingredient_input = st.text_input("Enter ingredients (comma-separated):")
    if ingredient_input:
        ingredients = [ingredient.strip() for ingredient in ingredient_input.split(",")]
        st.write("Ingredients added:", ingredients)

with tab2:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        with st.spinner("Processing image..."):
            st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
            # Here will will call the image processing function
            # ingredients = classify_ingredients(uploaded_file)
            # For now, we will simulate ingredient detection
            st.write("Ingredients detected:", ingredients)

headline= "INGREDIENTS"
if ingredients:
    if st.button("Generate Recipe"):
        with st.spinner("Generating recipe..."):
            generated = generation_function(ingredients)
            if generated:
                for text in generated:
                    sections = text.split("\n")
                    for section in sections:
                        section = section.strip()
                        if section.startswith("title:"):
                            section = section.replace("title:", "")
                            headline = "TITLE"
                        elif section.startswith("ingredients:"):
                            section = section.replace("ingredients:", "")
                            headline = "INGREDIENTS"
                        elif section.startswith("directions:"):
                            section = section.replace("directions:", "")
                            headline = "DIRECTIONS"
                        
                        if headline == "TITLE":
                            st.write(f"[{headline}]: {section.strip().capitalize()}")
                        else:
                            section_info = [f"  - {i+1}: {info.strip().capitalize()}" for i, info in enumerate(section.split("--"))]
                            st.write(f"[{headline}]:")
                            st.write("\n".join(section_info))
                else:
                    st.write("No recipe generated. Please try again with different ingredients.")


    
    

st.sidebar.header("About")
st.sidebar.write("Meal Buddy is your personal assistant for meal planning. Upload your ingredients or an image, and let us help you create a delicious recipe!")


