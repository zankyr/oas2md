from dataclasses import dataclass, field

@dataclass
class ResponseAttribute():
    name: str
    description: str = field(init=False, default=None)
    type: str = field(init=False, default=None)
    required: bool = field(init=False, default=False)
    example: str = field(init=False, default=None)