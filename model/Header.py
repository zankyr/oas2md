
from dataclasses import dataclass, field


@dataclass
class Header():
    name: str
    description: str = field(init=False, default=None)
    type: str = field(init=False, default=None)
    example: str = field(init=False, default=None)
