from ninja import Schema
from typing import List


class LoginRequestBody(Schema):
    email: str
    password: str


class AccessResponse(Schema):
    message: str
    access_token: str


class DecodeResponse(Schema):
    message: str
    user: str
    email: str
    groups: List[str]


class Error(Schema):
    error: str


class CsrfResponse(Schema):
    message: str
