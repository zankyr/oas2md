from dataclasses import dataclass


@dataclass
class Parameter:
    name: str = None
    location: str = None
    description: str = None
    type: str = None
    required: bool = False
    example: str = None
