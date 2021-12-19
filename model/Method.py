
from dataclasses import dataclass, field
from model.Request import Request

from model.Response import Response


@dataclass
class Method:
    method: str
    summary: str
    description: str
    request: Request = field(init=False, default=None)
    responses: list[Response] = field(init=False, default=None)
