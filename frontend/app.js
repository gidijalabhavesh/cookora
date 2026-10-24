const form = document.querySelector("#recipe-form");
const ingredientsInput = document.querySelector("#ingredients");
const ingredientCount = document.querySelector("#ingredient-count");
const generateButton = document.querySelector("#generate-button");
const buttonLabel = document.querySelector("#button-label");
const resultContent = document.querySelector("#result-content");
const resultError = document.querySelector("#result-error");

function countIngredients(value) {
  return [
    ...new Set(
      value
        .split(/[,\n]/)
        .map((ingredient) => ingredient.trim())
        .filter(Boolean)
        .map((ingredient) => ingredient.toLocaleLowerCase())
    ),
  ].length;
}

ingredientsInput.addEventListener("input", () => {
  const count = countIngredients(ingredientsInput.value);
  ingredientCount.textContent = `${count} entered`;
  ingredientCount.classList.toggle("count-warning", count > 50);
});

function showError(message) {
  resultContent.hidden = true;
  resultError.textContent = message;
  resultError.hidden = false;
}

function showRecipe(recipe) {
  resultError.hidden = true;
  resultContent.replaceChildren();
  resultContent.classList.add("has-recipe");

  const kicker = document.createElement("p");
  kicker.className = "result-kicker";
  kicker.textContent = "Made for your kitchen";

  const title = document.createElement("h2");
  title.textContent = "Your recipe is ready.";

  const content = document.createElement("pre");
  content.className = "recipe-text";
  content.textContent = recipe;

  resultContent.append(kicker, title, content);
  resultContent.hidden = false;
}

async function readError(response) {
  try {
    const body = await response.json();
    if (typeof body.detail === "string") {
      return body.detail;
    }
  } catch {
    return "The recipe service returned an unreadable response. Please try again.";
  }

  return `Recipe generation failed (HTTP ${response.status}). Please try again.`;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const ingredientText = ingredientsInput.value.trim();
  const count = countIngredients(ingredientText);

  if (!ingredientText || count === 0) {
    showError("Add at least one ingredient to get started.");
    ingredientsInput.focus();
    return;
  }

  if (count > 50) {
    showError("Please enter no more than 50 unique ingredients.");
    ingredientsInput.focus();
    return;
  }

  const apiBaseUrl = window.RECIPE_API_URL || window.location.origin;
  generateButton.disabled = true;
  buttonLabel.textContent = "Finding your recipe...";
  resultError.hidden = true;
  resultContent.hidden = true;

  try {
    const response = await fetch(`${apiBaseUrl}/api/recipes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ingredients: ingredientText,
        cuisine: document.querySelector("#cuisine").value,
        servings: Number(document.querySelector("#servings").value),
        diet: document.querySelector("#diet").value,
        extra: document.querySelector("#extra").value.trim(),
      }),
    });

    if (!response.ok) {
      showError(await readError(response));
      return;
    }

    const body = await response.json();
    if (typeof body.recipe !== "string" || !body.recipe.trim()) {
      showError("The recipe service returned an empty recipe. Please try again.");
      return;
    }
    showRecipe(body.recipe);
  } catch {
    showError(
      "We couldn’t reach the recipe service. Check your connection and try again."
    );
  } finally {
    generateButton.disabled = false;
    buttonLabel.textContent = "Find my recipe";
  }
});
