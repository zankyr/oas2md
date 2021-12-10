
from dataclasses import dataclass, field

from model.Response import Response


@dataclass
class Method():
    method: str
    summary: str
    description: str
    request: str = field(init=False, default=None)
    response: Response = field(init=False, default=None)
