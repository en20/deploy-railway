from api.application.ports.tokenPort import ITokenUseCase

from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, timezone, date
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError,
    DecodeError,
    InvalidSignatureError,
)


class TokenUseCase(ITokenUseCase):
    private_key: str
    public_key: str
    access_token_expiration: date
    refresh_token_expiration: date

    def __init__(
        self,
        access_token_expiration: date = timedelta(minutes=30),
        refresh_token_expiration: date = timedelta(days=14),
    ) -> None:
        load_dotenv()
        self.private_key = os.environ.get("PRIVATE_KEY")
        self.public_key = os.environ.get("PUBLIC_KEY")
        self.access_token_expiration = access_token_expiration
        self.refresh_token_expiration = refresh_token_expiration

    def generate_token(
        self, userId: str, email: str, groups: list[str], token_type: str
    ) -> str:
        expiration = 0
        if token_type == "access_token":
            expiration = self.access_token_expiration

        if token_type == "refresh_token":
            expiration = self.refresh_token_expiration

        token_payload = {
            "user": userId,
            "type": token_type,
            "email": email,
            "groups": groups,
            "exp": datetime.now(timezone.utc) + expiration,
            "iat": datetime.now(timezone.utc),
        }

        jwt_token = jwt.encode(token_payload, self.private_key, algorithm="RS256")

        return jwt_token

    def decode_token(self, token: str):
        return jwt.decode(token, self.public_key, algorithms="RS256")

    def verify_token(self, token: str, token_type: str) -> tuple[bool, str]:
        try:
            payload = jwt.decode(token, self.public_key, algorithms="RS256")

            if payload["type"] != token_type:
                return (False, "incorrect token type")

            return (True, "valid token")

        except InvalidSignatureError:
            return (False, "invalid signature")

        except ExpiredSignatureError:
            return (False, "token expired")

        except InvalidTokenError:
            return (False, "invalid token")
