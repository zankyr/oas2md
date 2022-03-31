from dataclasses import dataclass

from model.Content import Content
from model.Parameter import Parameter


@dataclass
class Request:
    parameters: list[Parameter] = None
    content: list[Content] = None
