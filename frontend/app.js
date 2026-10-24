const recipeForm = document.querySelector("#recipe-form");
const submitButton = document.querySelector("#submit-button");
const formMessage = document.querySelector("#form-message");
const resultContent = document.querySelector("#result-content");
const apiBaseUrl = (window.RECIPE_API_URL || "").replace(/\/+$/, "");

function showMessage(message, isError = false) {
  formMessage.textContent = message;
  formMessage.classList.toggle("error", isError);
}

recipeForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  showMessage("");

  const formData = new FormData(recipeForm);
  const ingredients = String(formData.get("ingredients") || "").trim();
  if (!ingredients) {
    showMessage("Add at least one ingredient to get started.", true);
    return;
  }

  submitButton.disabled = true;
  submitButton.querySelector("span:first-child").textContent = "Finding your recipe…";
  resultContent.classList.add("is-loading");

  try {
    const response = await fetch(`${apiBaseUrl}/api/recipes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ingredients,
        cuisine: formData.get("cuisine"),
        servings: Number(formData.get("servings")),
        diet: formData.get("diet"),
        extra: formData.get("extra"),
      }),
    });

    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error(
        "The recipe service returned an unexpected response. Check the Render API URL configuration.",
      );
    }
    if (!response.ok) {
      throw new Error(data.detail || "The recipe service could not complete your request.");
    }

    const heading = document.createElement("h2");
    heading.id = "result-title";
    heading.textContent = "Your recipe";
    const recipe = document.createElement("pre");
    recipe.className = "recipe-text";
    recipe.textContent = data.recipe;
    resultContent.replaceChildren(heading, recipe);
    showMessage("");
  } catch (error) {
    showMessage(
      error instanceof TypeError
        ? "Could not reach the recipe service. Check your connection and API configuration."
        : error.message,
      true,
    );
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector("span:first-child").textContent = "Find my recipe";
    resultContent.classList.remove("is-loading");
  }
});