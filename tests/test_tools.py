import unittest

from tools import (
    estimate_cooking_time,
    parse_ingredients,
    validate_recipe_request,
)


class RecipeToolsTests(unittest.TestCase):
    def test_parse_ingredients_splits_lines_and_removes_duplicates(self):
        self.assertEqual(
            parse_ingredients(" rice, tomatoes\nRice,  salt "),
            ["rice", "tomatoes", "Rice", "salt"],
        )

    def test_validate_recipe_request_rejects_empty_ingredients(self):
        with self.assertRaisesRegex(ValueError, "At least one ingredient"):
            validate_recipe_request([], 2)

    def test_validate_recipe_request_checks_serving_limit(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 12"):
            validate_recipe_request(["rice"], 13)

    def test_estimate_cooking_time_adds_preparation_and_cooking(self):
        self.assertEqual(estimate_cooking_time(10, 25), 35)

    def test_estimate_cooking_time_rejects_negative_values(self):
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            estimate_cooking_time(-1, 5)


if __name__ == "__main__":
    unittest.main()