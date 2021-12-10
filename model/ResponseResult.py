
from dataclasses import dataclass, field

from model.Header import Header


@dataclass
class ResponseResult():
    code: int
    description: str
    headers: list[Header]
