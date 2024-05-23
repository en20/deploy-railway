from django.test import TestCase

from api.adapters.outbound.database.models.group import Group
from api.adapters.outbound.database.repositories.GroupRepository import (
    GroupRepository,
)


group_repo = GroupRepository()


class TestGroupRepository(TestCase):

    def test_group_create(self):

        # Arrange
        test_group = group_repo.create(name="autobots", description="this is a test")

        # Act and Assert
        self.assertIsNotNone(test_group)
        self.assertEqual(test_group.name, "autobots")
        self.assertEqual(test_group.description, "this is a test")

    def test_group_update(self):

        # Arrange
        test_group = group_repo.create(name="autobots", description="this is a test")

        # Act
        u_result = group_repo.update(test_group.id, "the_jons", "not being baianos")
        id_result = group_repo.findById(test_group.id)

        # Assert
        self.assertEqual(True, u_result)
        self.assertEqual(id_result.name, "the_jons")
        self.assertEqual(id_result.description, "not being baianos")

    def test_group_delete(self):
        # Arrange
        test_group = group_repo.create(name="autobots", description="this is a test")

        # Act
        result = group_repo.delete(test_group.id)

        # Assert
        self.assertEqual(True, result)

    def test_group_find_by_id(self):

        # Arrange
        test_group = group_repo.create(name="autobots", description="this is a test")

        # Act
        result = group_repo.findById(test_group.id)

        # Assert
        self.assertEqual(test_group, result)

    def test_group_find_all(self):

        # Arrange
        test_group_one = group_repo.create(
            name="autobots", description="this is a test"
        )
        test_group_two = group_repo.create(
            name="autobots", description="this is a test"
        )

        # Act
        check_list = group_repo.findAll(0, 2)

        # Assert
        self.assertEquals(check_list[0], test_group_one)
        self.assertEquals(check_list[1], test_group_two)
