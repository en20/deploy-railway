from ninja import Router, Body, File
from ninja.files import UploadedFile
from pydantic import BaseModel
from django.http import HttpRequest
from api.adapters.inbound.http.dtos.Auth import Error
from api.adapters.inbound.http.utils.Task import validate_request
from typing import Any, List, Optional


class Ok(BaseModel):
    message: str


class Schema01(BaseModel):
    message: str
    number: int


class Schema02(BaseModel):
    message: str
    number_list: List[int]


class Schema03(BaseModel):
    message: str
    dictionary: dict[str, Any]


class MockController:
    def get_router(self):
        router = Router()

        @router.post("/validate", response={200: Ok, 400: Error})
        @validate_request(key="data", schemas=[Schema01, Schema02, Schema03])
        def validate(
            request: HttpRequest,
            data: dict[str, Any] = Body(...),
            file: Optional[UploadedFile] = File(None),
        ):
            return {"message": "Schema validated successfully"}

        return router
