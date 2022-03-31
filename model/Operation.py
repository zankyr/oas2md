
from dataclasses import dataclass, field

from model.Request import Request
from model.Response import Response


@dataclass
class Operation:
    operation: str
    summary: str = None
    description: str = None
    request: Request = field(init=False, default=None)
    responses: list[Response] = field(init=False, default=None)
