from django.test import SimpleTestCase
from json import dumps


class TestRequestValidation(SimpleTestCase):
    def test_validate_schema_one(self):
        # Arrange
        schema_one = dumps({"message": "schema_one", "number": 77})
        # Act
        response = self.client.post(
            "/api/test/validate",
            {"data": schema_one},
        )
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Schema validated successfully")

    def test_validate_schema_two(self):
        # Arrange
        schema_two = dumps({"message": "schema_one", "number_list": [1, 2, 3, 4, 5]})
        # Act
        response = self.client.post(
            "/api/test/validate",
            {"data": schema_two},
        )
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Schema validated successfully")

    def test_validate_schema_three(self):
        # Arrange
        schema_three = dumps(
            {"message": "schema_one", "dictionary": {"arg1": "hello", "arg2": "world"}}
        )
        # Act
        response = self.client.post(
            "/api/test/validate",
            {"data": schema_three},
        )
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Schema validated successfully")

    def test_validate_invalid_schema(self):
        # Arrange
        unknown_schema = dumps({"message": "schema_one", "unknown": "value"})
        # Act
        response = self.client.post(
            "/api/test/validate",
            {"data": unknown_schema},
        )
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Unknown schema provided")
