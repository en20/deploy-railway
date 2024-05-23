from datetime import timedelta, datetime, timezone
from api.application.usecases.tokenUseCase import TokenUseCase
from django.test import SimpleTestCase


class TestUseCaseAuthentication(SimpleTestCase):

    def setUp(self):
        self.token_use_case = TokenUseCase()

    def test_generate_access_token(self):
        # Arrange / Act
        token = self.token_use_case.generate_token(
            "user_id", "user@example.com", ["group1", "group2"], "access_token"
        )
        # Assert
        self.assertIsInstance(token, str)

    def test_generate_refresh_token(self):
        # Arrange / Act
        token = self.token_use_case.generate_token(
            "user_id", "user@example.com", ["group1", "group2"], "refresh_token"
        )
        # Assert
        self.assertIsInstance(token, str)

    def test_decode_token(self):
        # Arrange
        token = self.token_use_case.generate_token(
            "user_id", "user@example.com", ["group1", "group2"], "access_token"
        )
        # Act
        decoded_token = self.token_use_case.decode_token(token)
        # Assert
        self.assertEqual(decoded_token["user"], "user_id")
        self.assertEqual(decoded_token["email"], "user@example.com")
        self.assertEqual(decoded_token["type"], "access_token")
        self.assertEqual(decoded_token["groups"], ["group1", "group2"])

    def test_verify_valid_token(self):
        # Arrange
        token = self.token_use_case.generate_token(
            "user_id", "user@example.com", ["group1", "group2"], "access_token"
        )
        # Act
        result, message = self.token_use_case.verify_token(token, "access_token")
        # Assert
        self.assertTrue(result)
        self.assertEqual(message, "valid token")

    def test_verify_invalid_token_type(self):
        # Arrange
        token = self.token_use_case.generate_token(
            "user_id", "user@example.com", ["group1", "group2"], "access_token"
        )
        # Act
        result, message = self.token_use_case.verify_token(token, "refresh_token")
        # Assert
        self.assertFalse(result)
        self.assertEqual(message, "incorrect token type")

    def test_expired_token(self):
        # Arrange
        self.token_use_case.access_token_expiration = timedelta(seconds=0)
        token = self.token_use_case.generate_token(
            "user_id", "user@example.com", ["group1", "group2"], "access_token"
        )
        # Act
        result, message = self.token_use_case.verify_token(token, "access_token")
        # Assert
        self.assertFalse(result)
        self.assertEqual(message, "token expired")

        self.token_use_case.access_token_expiration = timedelta(minutes=30)
