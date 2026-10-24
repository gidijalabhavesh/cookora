
def parse_ingredients(text):
    """Convert comma-separated ingredients into a clean list."""
    if not text:
        return []

    ingredients = [
        item.strip()
        for item in text.replace("\n", ",").split(",")
        if item.strip()
    ]

    # Remove duplicates while preserving order.
    return list(dict.fromkeys(ingredients))


def validate_recipe_request(ingredients, servings):
    """Validate ingredients and serving count."""
    if not ingredients:
        raise ValueError("At least one ingredient is required.")

    if not isinstance(servings, int) or not 1 <= servings <= 12:
        raise ValueError("Servings must be between 1 and 12.")

    if len(ingredients) > 50:
        raise ValueError("Please enter no more than 50 ingredients.")

    return True


def estimate_cooking_time(preparation_minutes, cooking_minutes):
    """Calculate the total estimated cooking time."""
    if preparation_minutes < 0 or cooking_minutes < 0:
        raise ValueError("Cooking times cannot be negative.")

    return preparation_minutes + cooking_minutes
