import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api import app


class RecipeApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_homepage_is_served(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Pantry", response.text)

    def test_health_check_does_not_expose_api_key(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertNotIn("OPENAI_API_KEY", response.text)

    def test_recipe_request_rejects_empty_ingredients(self):
        response = self.client.post(
            "/api/recipes",
            json={"ingredients": " , \n ", "servings": 2},
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("At least one ingredient", response.json()["detail"])

    def test_missing_api_key_returns_service_unavailable(self):
        with patch("api.generate_recipe", side_effect=RuntimeError("API key missing")):
            response = self.client.post(
                "/api/recipes",
                json={"ingredients": "rice", "servings": 2},
            )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "API key missing")

    def test_recipe_request_returns_generated_recipe(self):
        with patch("api.generate_recipe", return_value="Tomato rice"):
            response = self.client.post(
                "/api/recipes",
                json={
                    "ingredients": "rice, tomato",
                    "cuisine": "Indian",
                    "servings": 2,
                    "diet": "Vegetarian",
                    "extra": "quick",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"recipe": "Tomato rice"})


if __name__ == "__main__":
    unittest.main()
