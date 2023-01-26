import os
from datetime import datetime, timedelta
from typing import List, Literal, Optional

from jose import jwt
from jose.constants import ALGORITHMS


class JwtToken:
    def __init__(self) -> None:
        self.token_expire = int(os.getenv("JWT_TOKEN_EXPIRE"))
        self.refresh_token_expire = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE"))
        self.secret_key = os.getenv("JWT_SECRET_KEY")

    def encode(
        self,
        user_id: int,
        token_type: Literal["TOKEN", "REFRESH_TOKEN"],
        permissions: List[Literal["ADM", "PLAYER", "REFRESH"]],
    ) -> str:
        match token_type:
            case "TOKEN":
                expire_in = self.token_expire
            case "REFRESH_TOKEN":
                expire_in = self.refresh_token_expire
            case _:
                raise ValueError
        return jwt.encode(
            claims={
                "permissions": permissions,
                "user": user_id,
                "exp": datetime.timestamp(datetime.now() + timedelta(hours=expire_in)),
            },
            key=self.secret_key,
            algorithm=ALGORITHMS.HS512,
        )

    def decode(self, token: str, options: Optional[dict] = None):
        if options:
            return jwt.decode(
                token=token,
                key=self.secret_key,
                algorithms=ALGORITHMS.HS512,
                options=options,
            )
        return jwt.decode(
            token=token,
            key=self.secret_key,
            algorithms=ALGORITHMS.HS512,
        )
