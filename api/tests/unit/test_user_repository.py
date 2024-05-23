from django.test import TestCase

from api.adapters.outbound.database.models.user import User
from api.adapters.outbound.database.repositories.UserRepository import (
    UserRepository,
)

user_repo = UserRepository()


class TestGroupRepository(TestCase):

    def test_user_creation(self):

        # Arrange
        test_user = user_repo.create(
            name="autobots", email="jon@gmail.com", password="galindo"
        )

        # Act and Assert
        self.assertIsNotNone(test_user)
        self.assertEqual(test_user.name, "autobots")
        self.assertEqual(test_user.email, "jon@gmail.com")
        self.assertEqual(test_user.password, "galindo")

    def test_user_update(self):

        # Arrange
        test_user = user_repo.create(
            name="autobots", email="jon@gmail.com", password="galindo"
        )

        # Act
        u_result = user_repo.update(
            test_user.id, "the_jons", "nonjon@gmail.com", "galo"
        )
        id_result = user_repo.findById(test_user.id)

        # Assert
        self.assertEqual(True, u_result)
        self.assertEqual(id_result.name, "the_jons")
        self.assertEqual(id_result.email, "nonjon@gmail.com")
        self.assertEqual(id_result.password, "galo")

    def test_user_delete(self):
        # Arrange
        test_user = user_repo.create(
            name="autobots", email="jon@gmail.com", password="galindo"
        )

        # Act
        result = user_repo.delete(test_user.id)

        # Assert
        self.assertEqual(True, result)

    def test_user_find_by_id(self):

        # Arrange
        test_user = user_repo.create(
            name="autobots", email="jon@gmail.com", password="galindo"
        )

        # Act
        result = user_repo.findById(test_user.id)

        # Assert
        self.assertEqual(test_user, result)

    def test_user_find_by_email(self):
        # Arrange
        test_user = user_repo.create(
            name="autobots", email="jon@gmail.com", password="galindo"
        )

        # Act
        result = user_repo.findByEmail(test_user.email)

        # Assert
        self.assertEqual(test_user, result)

    def test_user_find_all(self):

        # Arrange
        test_user_one = user_repo.create(
            name="autobots", email="jon@gmail.com", password="galindo"
        )
        test_user_two = user_repo.create(
            name="autobots", email="jon@gmail.com", password="galindo"
        )

        # Act
        check_list = user_repo.findAll(0, 2)

        # Assert
        self.assertEquals(check_list[0], test_user_one)
        self.assertEquals(check_list[1], test_user_two)
