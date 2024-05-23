from api.application.ports.runPort import IRunUseCase
from api.domain.entities.run import Run
from api.domain.entities.robot import Robot
from api.adapters.outbound.database.repositories.RunRepository import RunRepository
from api.adapters.outbound.database.repositories.RobotRepository import RobotRepository


class RunUseCase(IRunUseCase):
    runRepository: RunRepository
    robotRepository: RobotRepository

    def __init__(
        self, runRepository: RunRepository, robotRepository: RobotRepository
    ) -> None:
        self.runRepository = runRepository
        self.robotRepository = robotRepository

    def createRun(self, robot: Robot, task: str) -> Run:
        robotSchema = self.robotRepository.robotToSchema(robot)
        return self.runRepository.create(task, robotSchema)

    def getRobotRuns(self, robot, skip, limit) -> list[Run]:
        return self.runRepository.getRobotRuns(robot)

    def getRunById(self, runId) -> Run:
        return self.runRepository.findById(runId)

    def countRobotRuns(self, robot) -> int:
        return self.runRepository.countRobotRuns(robot)

    def updateRunStatus(self, run: Run, status: str) -> bool:
        run = self.runRepository.runToSchema(run)
        return self.runRepository.update(run.id, run.task, run.robot, status)
