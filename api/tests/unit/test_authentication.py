from django.test import TestCase
from datetime import timedelta
import json
from api.tests.testApi import mockRepository, tokenUseCase


class AuthenticationTestCase(TestCase):
    def setUp(self):
        # Clean up mock repository
        for user in mockRepository.findAll(0, 0):
            mockRepository.delete(user.id)

    def test_user_login(self):
        """User should log in successfully"""

        # Arrange
        user = mockRepository.create("Jonn", "john@gmail.com", "galindo")
        # Act
        response = self.client.post(
            "/api/auth/login",
            json.dumps({"email": user.email, "password": user.password}),
            content_type="application/json",
        )
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "logged in successfully")

    def test_invalid_email(self):
        """Avoid logging in with invalid email"""
        # Arrange
        email = "invalid@gmail.com"
        password = "12345"
        # Act
        response = self.client.post(
            "/api/auth/login",
            json.dumps({"email": email, "password": password}),
            content_type="application/json",
        )
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Email invalido")

    def test_invalid_password(self):
        """Avoid logging in with invalid password"""
        # Arrange
        user = mockRepository.create("Jonn", "john@gmail.com", "galindo")
        # Act
        response = self.client.post(
            "/api/auth/login",
            json.dumps({"email": user.email, "password": "12345"}),
            content_type="application/json",
        )
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Senha incorreta")

    def test_valid_csrf(self):
        """Ensure that the csrf token is retrieved correctly"""

        # Act
        response = self.client.get("/api/auth/csrf")
        csrf_token = response.cookies["csrftoken"]

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue("csrftoken" in response.cookies)
        self.assertNotEqual(csrf_token, "")

    def test_valid_access_token(self):
        """Ensure the access token is a valid token"""

        # Arrange
        user = mockRepository.create("Jonn", "john@gmail.com", "galindo")

        response = self.client.post(
            "/api/auth/login",
            json.dumps({"email": user.email, "password": user.password}),
            content_type="application/json",
        )

        access_token = response.json()["access_token"]

        response = self.client.get(
            "/api/auth/decode",
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "message": "Token decoded successfully",
                "user": user.id,
                "email": user.email,
                "groups": user.groups,
            },
        )

    def test_invalid_access_token(self):
        """Ensure the token is invalid"""

        # Arrange
        invalid_access_token = "invalid_access_token"

        # Act
        response = self.client.get(
            "/api/auth/decode",
            HTTP_AUTHORIZATION=f"Bearer {invalid_access_token}",
        )

        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error": "invalid token"})

    def test_expired_access_token(self):
        """Ensure the token does not give access to the endpoint"""

        # Arrange
        tokenUseCase.access_token_expiration = timedelta(seconds=0)

        user = mockRepository.create("Jonn", "john@gmail.com", "galindo")

        response = self.client.post(
            "/api/auth/login",
            json.dumps({"email": user.email, "password": user.password}),
            content_type="application/json",
        )

        access_token = response.json()["access_token"]

        # Act
        response = self.client.get(
            "/api/auth/decode",
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error": "token expired"})

        # Change back to 30 minutes
        tokenUseCase.access_token_expiration = timedelta(minutes=30)

    def test_refresh_endpoint(self):
        """Ensure the token refreshes successfully"""

        # Arrange
        tokenUseCase.refresh_token_expiration = timedelta(days=14)

        user = mockRepository.create("Jonn", "john@gmail.com", "galindo")

        response = self.client.post(
            "/api/auth/login",
            json.dumps({"email": user.email, "password": user.password}),
            content_type="application/json",
        )

        refresh_token = response.cookies["refresh_token"].value

        # Act
        self.client.cookies.load({"refresh_token": refresh_token})
        refresh_response = self.client.get("/api/auth/refresh")

        access_token = refresh_response.json()["access_token"]

        decode_response = self.client.get(
            "/api/auth/decode",
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        # Assert
        self.assertEqual(refresh_response.status_code, 200)
        self.assertEqual(decode_response.status_code, 200)
        self.assertEqual(
            refresh_response.json()["message"], "Token refreshed successfully"
        )
        self.assertEqual(
            decode_response.json(),
            {
                "message": "Token decoded successfully",
                "user": user.id,
                "email": user.email,
                "groups": user.groups,
            },
        )

    def test_invalid_refresh_token(self):
        """Ensure refresh does not work without the cookie"""

        # Act
        response = self.client.get("/api/auth/refresh")

        # Assert
        self.assertEqual(response.json()["error"], "cookie not found")

    def test_expired_refresh_token(self):
        """Ensure the endpoint doesn't work when the refresh token is expired"""

        # Arrange
        tokenUseCase.refresh_token_expiration = timedelta(seconds=0)

        user = mockRepository.create("Jonn", "john@gmail.com", "galindo")

        response = self.client.post(
            "/api/auth/login",
            json.dumps({"email": user.email, "password": user.password}),
            content_type="application/json",
        )

        refresh_token = response.cookies["refresh_token"].value

        # Act
        self.client.cookies.load({"refresh_token": refresh_token})

        refresh_response = self.client.get("/api/auth/refresh")

        # Assert
        self.assertEqual(refresh_response.status_code, 401)
        self.assertEqual(refresh_response.json()["error"], "token expired")

        # Change back to 14 days
        tokenUseCase.refresh_token_expiration = timedelta(days=14)
