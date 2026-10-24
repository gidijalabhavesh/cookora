
import streamlit as st
from model import generate_recipe
from tools import parse_ingredients

st.set_page_config(
    page_title="Smart Recipe Generator AI",
    page_icon="🍲",
    layout="centered"
)

st.title("🍲 Smart Recipe Generator AI")
st.write("Turn the ingredients in your kitchen into delicious recipes!")

ingredients_text = st.text_area(
    "🥕 What ingredients do you have?",
    placeholder="Example: rice, onions, tomatoes, eggs",
    height=120
)

col1, col2 = st.columns(2)

with col1:
    cuisine = st.selectbox(
        "Choose cuisine",
        ["Indian", "South Indian", "Italian", "Chinese", "Any"]
    )

with col2:
    servings = st.number_input(
        "Number of servings",
        min_value=1,
        max_value=12,
        value=2
    )

diet = st.selectbox(
    "Dietary preference",
    ["No preference", "Vegetarian", "Vegan", "Egg-based"]
)

extra = st.text_input(
    "Optional preferences",
    placeholder="Example: spicy, quick, low-cost"
)

if st.button("✨ Generate Recipe", use_container_width=True):
    ingredients = parse_ingredients(ingredients_text)

    if not ingredients:
        st.warning("Please enter at least one ingredient.")
    else:
        with st.spinner("Creating your recipe..."):
            try:
                recipe = generate_recipe(
                    ingredients=ingredients,
                    cuisine=cuisine,
                    servings=servings,
                    diet=diet,
                    extra=extra
                )

                st.markdown("---")
                st.subheader("👨‍🍳 Your AI-Generated Recipe")
                st.markdown(recipe)

            except Exception as error:
                st.error(f"Recipe generation failed: {error}")
                st.info(
                    "Check your API key, internet connection, "
                    "and model settings."
                )

st.markdown("---")
st.caption("Smart Recipe Generator AI | Built with Python and Streamlit")
