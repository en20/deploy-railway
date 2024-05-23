from django.test import TestCase


from api.adapters.outbound.database.repositories.GroupRepository import GroupRepository
from api.adapters.outbound.database.repositories.RobotRepository import RobotRepository

robot_repo = RobotRepository()
group_repo = GroupRepository()


class TestGroupRepository(TestCase):

    def test_robot_create(self):

        # Arrange

        test_group = group_repo.rawCreate(name="autobots", description="this is a test")

        test_robot = robot_repo.create(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )

        # Act and Assert
        self.assertIsNotNone(test_robot)
        self.assertEqual(test_robot.name, "autobots")
        self.assertEqual(test_robot.description, "this is a test")
        self.assertEqual(test_robot.section_name, "test")
        self.assertEqual(test_robot.group, test_group.id)

    def test_robot_update(self):

        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.create(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        # Act
        u_result = robot_repo.update(
            test_robot.id, "the_jons", "not being baianos", "new test", test_group
        )
        id_result = robot_repo.findById(test_robot.id)

        # Assert
        self.assertEqual(True, u_result)
        self.assertEqual(id_result.name, "the_jons")
        self.assertEqual(id_result.description, "not being baianos")
        self.assertEqual(id_result.section_name, "new test")
        self.assertEqual(id_result.group, test_group.id)

    def test_robot_delete(self):
        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.create(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        # Act
        result = robot_repo.delete(test_robot.id)

        # Assert
        self.assertEqual(True, result)

    def test_robot_find_by_id(self):

        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.create(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )

        # Act
        result = robot_repo.findById(test_robot.id)

        # Assert
        self.assertEqual(test_robot, result)

    def test_robot_find_all(self):

        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot_one = robot_repo.create(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        test_robot_two = robot_repo.create(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )

        # Act
        check_list = robot_repo.findAll(0, 2)

        # Assert
        self.assertEquals(check_list[0], test_robot_one)
        self.assertEquals(check_list[1], test_robot_two)

    def test_robot_find_all_by_groups(self):
        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot_one = robot_repo.create(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        test_robot_two = robot_repo.create(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )

        # Act

        base_list = [test_robot_one, test_robot_two]
        check_list = robot_repo.findAllByGroups([test_group.id])
        # Assert
        self.assertEquals(check_list, base_list)
