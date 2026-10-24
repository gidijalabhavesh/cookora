
import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import validate_recipe_request

load_dotenv()


def generate_recipe(ingredients, cuisine, servings, diet, extra=""):
    validate_recipe_request(ingredients, servings)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to your .env file."
        )

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are Smart Recipe Generator AI, a helpful cooking assistant.

Available ingredients: {", ".join(ingredients)}
Cuisine: {cuisine}
Servings: {servings}
Dietary preference: {diet}
Additional preferences: {extra or "None"}

Create one practical recipe using the available ingredients.

Include:
1. Recipe name
2. Short description
3. Preparation time and cooking time
4. Ingredients with quantities for the requested servings
5. Numbered cooking instructions
6. Useful cooking tips
7. Possible substitutions for missing ingredients

Rules:
- Respect the dietary preference.
- Clearly identify any additional ingredients required.
- Never invent exact nutrition values.
- Give safe food handling and cooking instructions.
- Flag common allergens when relevant.
- Do not claim a recipe is allergen-free without verification.
- If the ingredients are insufficient, explain what is missing.
- Use clear, beginner-friendly language.
"""

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt
    )

    return response.output_text
