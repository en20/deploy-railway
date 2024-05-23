from django.test import SimpleTestCase


class TestProtectedRoute(SimpleTestCase):
    def test_the_robot_route_is_protected(self):
        """ " Ensure the route is protected"""

        # Arrange
        invalid_token = "invalid_token"

        # Act
        route_response = self.client.get(
            "/api/robot/", HTTP_AUTHORIZATION=f"Bearer {invalid_token}"
        )

        # Assert
        self.assertEqual(route_response.status_code, 401)
