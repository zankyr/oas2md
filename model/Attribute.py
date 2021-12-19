from dataclasses import dataclass, field


@dataclass
class Attribute:
    name: str
    parent_attribute: str = field(init=False, default=None)
    description: str = field(init=False, default=None)
    type: str = field(init=False, default=None)
    required: bool = field(init=False, default=False)
    example: str = field(init=False, default=None)
