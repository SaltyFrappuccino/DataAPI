from fastapi import Header


class GeneralHeadersModel:
    def __init__(
        self,
        authorization: str | None = Header(None, alias="Authorization")
    ):
        self.authorization = authorization
