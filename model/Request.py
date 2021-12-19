from dataclasses import dataclass

from model.Content import Content


@dataclass
class Request:
    content: list[Content]
