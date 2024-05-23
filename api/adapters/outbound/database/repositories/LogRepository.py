from api.adapters.outbound.database.models.log import Log as LogSchema
from api.domain.entities.log import Log
from api.domain.repositories.ILogRepository import ILogRepository
from django.core.exceptions import ObjectDoesNotExist
from api.adapters.outbound.database.models.run import Run as RunSchema


# Concrete implementation for Log repository
class LogRepository(ILogRepository):
    def create(self, run: RunSchema, content: str, level: str) -> Log:
        return self.schemaToLog(
            LogSchema.objects.create(
                run=run,
                content=content,
                level=level,
            )
        )

    def rawCreate(self, run: RunSchema, content: str, level: str) -> LogSchema:
        return LogSchema.objects.create(
            run=run,
            content=content,
            level=level,
        )

    def update(self, id: str, run: RunSchema, content: str, level: str) -> bool:
        try:
            LogSchema.objects.filter(id=id).update(
                run=run,
                content=content,
                level=level,
            )
            return True
        except ObjectDoesNotExist:
            return False

    def delete(self, id) -> bool:
        try:
            LogSchema.objects.filter(id=id).delete()
            return True
        except ObjectDoesNotExist:
            return False

    def findById(self, id) -> Log:
        return self.schemaToLog(LogSchema.objects.get(id=id))

    def findAll(self, skip, limit) -> list[Log]:
        return list(map(self.schemaToLog, LogSchema.objects.all()[skip:limit]))

    def get_logs_by_run_id(self, run_id) -> list[Log]:
        return list(map(self.schemaToLog, LogSchema.objects.filter(run=run_id)))

    def count_logs_by_run_id(self, run_id) -> int:
        return LogSchema.objects.filter(run=run_id).count()

    def schemaToLog(self, schema: LogSchema) -> Log:
        return Log(
            schema.id,
            schema.run.id,
            schema.content,
            schema.level,
            str(schema.executed_at),
        )

    def logToSchema(self, log: Log) -> LogSchema:
        try:
            return LogSchema.objects.get(id=log.id)
        except ObjectDoesNotExist:
            return None
