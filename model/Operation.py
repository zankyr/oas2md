
from dataclasses import dataclass, field

from model.Request import Request
from model.Response import Response


@dataclass
class Operation:
    operation: str
    summary: str = field(init=False, default=None)
    description: str = field(init=False, default=None)
    request: Request = field(init=False, default=None)
    responses: list[Response] = field(init=False, default=None)
