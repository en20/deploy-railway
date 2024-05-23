from django.test import TestCase

from api.adapters.outbound.database.models.log import Log
from api.adapters.outbound.database.repositories.LogRepository import LogRepository
from api.adapters.outbound.database.repositories.RunRepository import RunRepository
from api.adapters.outbound.database.repositories.GroupRepository import GroupRepository
from api.adapters.outbound.database.repositories.RobotRepository import RobotRepository

run_repo = RunRepository()
robot_repo = RobotRepository()
group_repo = GroupRepository()
log_repo = LogRepository()


class TestLogRepository(TestCase):

    def test_log_create(self):
        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.rawCreate(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        test_run = run_repo.rawCreate(task="autobots", robot=test_robot)
        test_log = log_repo.create(run=test_run, content="this is a test", level="jon")

        # Act and Assert
        self.assertIsNotNone(test_log)
        self.assertEqual(test_log.run, test_run.id)
        self.assertEqual(test_log.content, "this is a test")
        self.assertEqual(test_log.level, "jon")

    def test_log_update(self):

        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.rawCreate(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        test_run = run_repo.rawCreate(task="autobots", robot=test_robot)
        new_test_run = run_repo.rawCreate(task="notautobots", robot=test_robot)
        test_log = log_repo.create(run=test_run, content="this is a test", level="jon")

        # Act
        u_result = log_repo.update(
            test_log.id, new_test_run, "not being baianos", "the_jons"
        )
        id_result = log_repo.findById(test_log.id)

        # Assert
        self.assertEquals(True, u_result)
        self.assertEqual(id_result.run, new_test_run.id)
        self.assertEqual(id_result.content, "not being baianos")
        self.assertEqual(id_result.level, "the_jons")

    def test_log_delete(self):
        # Arrange

        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.rawCreate(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        test_run = run_repo.rawCreate(task="autobots", robot=test_robot)
        test_log = log_repo.create(run=test_run, content="this is a test", level="jon")

        # Act
        result = log_repo.delete(test_log.id)

        # Assert
        self.assertEqual(True, result)

    def test_log_find_by_id(self):

        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.rawCreate(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        test_run = run_repo.rawCreate(task="autobots", robot=test_robot)
        test_log = log_repo.create(run=test_run, content="this is a test", level="jon")

        # Act
        result = log_repo.findById(test_log.id)

        # Assert
        self.assertEqual(test_log, result)

    def test_log_find_all(self):

        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.rawCreate(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        test_run = run_repo.rawCreate(task="autobots", robot=test_robot)
        new_test_run = run_repo.rawCreate(task="notautobots", robot=test_robot)
        test_log_one = log_repo.create(
            run=test_run, content="this is a test", level="jon"
        )
        test_log_two = log_repo.create(
            run=new_test_run, content="not being baianos", level="the_jons"
        )

        # Act
        check_list = log_repo.findAll(0, 2)

        # Assert
        self.assertEquals(check_list[0], test_log_one)
        self.assertEquals(check_list[1], test_log_two)

    def test_log_get_logs_by_run_id(self):

        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.rawCreate(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        test_run = run_repo.rawCreate(task="autobots", robot=test_robot)
        test_log_one = log_repo.create(
            run=test_run, content="this is a test", level="jon"
        )
        test_log_two = log_repo.create(
            run=test_run, content="this is not a test", level="nonjon"
        )

        # Act
        check = log_repo.get_logs_by_run_id(test_run.id)

        # Assert
        self.assertEquals(check[0], test_log_one)
        self.assertEquals(check[1], test_log_two)

    def test_log_count_logs_by_run_id(self):
        # Arrange
        test_group = group_repo.rawCreate(name="autobots", description="this is a test")
        test_robot = robot_repo.rawCreate(
            name="autobots",
            description="this is a test",
            section_name="test",
            group=test_group,
        )
        test_run = run_repo.rawCreate(task="autobots", robot=test_robot)
        test_log_one = log_repo.create(
            run=test_run, content="this is a test", level="jon"
        )
        test_log_two = log_repo.create(
            run=test_run, content="this is not a test", level="nonjon"
        )

        count = log_repo.count_logs_by_run_id(test_run.id)
        self.assertEquals(2, count)
