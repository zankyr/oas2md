from dataclasses import dataclass

from model.Header import Header
from model.Content import Content


@dataclass
class Response:
    code: int
    description: str
    headers: list[Header]
    content: list[Content]
